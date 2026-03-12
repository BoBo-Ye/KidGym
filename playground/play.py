import os
import sys
import gymnasium as gym
import gradio as gr

# -----------------------------
# Path hack: allow `import tasks` from parent dir
# -----------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import tasks  # noqa: F401  # ensure env registration happens on import

TASKS = ["CL", "PU", "CO", "PL", "SO", "FI", "MA", "DE", "SE", "MMA", "MFI", "MDE", "DMA"]
LEVELS = ["1", "2", "3"]


# -----------------------------
# Helpers
# -----------------------------
def _extract_obs(reset_out):
    # gymnasium reset: (obs, info), gym: obs
    if isinstance(reset_out, tuple) and len(reset_out) == 2:
        return reset_out[0]
    return reset_out


def _safe_render(env):
    try:
        return env.render()
    except Exception as e:
        gr.Warning(f"render() failed: {e}")
        return None


def _get_actions(env):
    return list(getattr(env, "actions", []))


def _update_action_radio(env, current_action=None):
    actions = _get_actions(env)
    if not actions:
        return gr.update(choices=[], value=None, interactive=False)
    value = current_action if (current_action in actions) else actions[0]
    return gr.update(choices=actions, value=value, interactive=True)


def _make_env(task: str, level: str):
    env_id = f"{task}_L{level}"
    env = gym.make(env_id).unwrapped
    return env


def _reset_env(env):
    obs = _extract_obs(env.reset())
    done = False
    frame = _safe_render(env)
    return obs, done, frame


def _notice(done: bool):
    return "✅ **本轮游戏已结束，请点击 Reset。**" if done else ""


# -----------------------------
# Callbacks
# -----------------------------
def on_load():
    # default selection
    task, level = "CL", "1"
    try:
        env = _make_env(task, level)
        obs, done, frame = _reset_env(env)
        action_update = _update_action_radio(env, None)
        return (
            env, obs, done,               # states
            frame,                        # image
            action_update,                # action radio
            task, level,                  # dropdown values
            _notice(done),                # episode notice
        )
    except Exception as e:
        gr.Warning(str(e))
        return (
            None, None, True,
            None,
            gr.update(choices=[], value=None, interactive=False),
            task, level,
            "⚠️ **环境加载失败，请检查任务注册与 env id。**",
        )


def on_task_or_level_change(task, level):
    try:
        env = _make_env(task, level)
        obs, done, frame = _reset_env(env)
        action_update = _update_action_radio(env, None)
        # 切换环境后，提示栏清空（done=False）
        return env, obs, done, frame, action_update, _notice(done)
    except Exception as e:
        gr.Warning(str(e))
        return (
            None, None, True,
            None,
            gr.update(choices=[], value=None, interactive=False),
            "⚠️ **环境切换失败，请检查该任务/难度是否存在。**",
        )


def on_step(env, obs, done, action):
    if env is None:
        gr.Warning("env is not initialized.")
        return None, obs, True, gr.update(), "⚠️ **环境未初始化，请重新选择任务/难度。**"

    if done:
        # 已结束：保持画面，提示栏显示结束信息
        frame = _safe_render(env)
        return frame, obs, done, _update_action_radio(env, action), _notice(True)

    actions = _get_actions(env)
    if not actions:
        gr.Warning("env.actions is empty.")
        frame = _safe_render(env)
        return frame, obs, done, _update_action_radio(env, action), ""

    if action not in actions:
        action = actions[0]
    action_id = actions.index(action)

    step_out = env.step(action_id)

    # gymnasium: (obs, reward, terminated, truncated, info)
    # gym:       (obs, reward, done, info)
    if isinstance(step_out, tuple) and len(step_out) == 5:
        obs2, reward, terminated, truncated, info = step_out
        done2 = bool(terminated or truncated)
    else:
        obs2, reward, done2, info = step_out
        done2 = bool(done2)

    frame = _safe_render(env)

    # refresh action list after step
    action_update = _update_action_radio(env, action)

    return frame, obs2, done2, action_update, _notice(done2)


def on_reset(env, current_action):
    if env is None:
        gr.Warning("env is not initialized.")
        return None, None, True, gr.update(), "⚠️ **环境未初始化，请重新选择任务/难度。**"

    obs2, done2, frame = _reset_env(env)
    action_update = _update_action_radio(env, current_action)
    # Reset 后清空提示
    return frame, obs2, done2, action_update, _notice(False)


# -----------------------------
# UI
# -----------------------------
with gr.Blocks(title="KidGym Playground") as demo:
    gr.Markdown("# KidGym Playground")

    # Per-user session states
    env_state = gr.State()
    obs_state = gr.State()
    done_state = gr.State()

    with gr.Row():
        task_dd = gr.Dropdown(label="任务", choices=TASKS, value="CL", interactive=True)
        level_dd = gr.Dropdown(label="难度", choices=LEVELS, value="1", interactive=True)

    # Episode end notice bar (persistent area)
    episode_notice = gr.Markdown("")

    img = gr.Image(label="Scene", type="numpy")

    action_radio = gr.Radio(label="请选择一个动作", choices=[], value=None, interactive=True)

    with gr.Row():
        btn_step = gr.Button("执行动作")
        btn_reset = gr.Button("Reset")

    # Load: init env + populate UI
    demo.load(
        on_load,
        inputs=None,
        outputs=[
            env_state, obs_state, done_state,
            img,
            action_radio,
            task_dd, level_dd,
            episode_notice,
        ],
    )

    # Change task/level => rebuild env and refresh everything
    task_dd.change(
        on_task_or_level_change,
        inputs=[task_dd, level_dd],
        outputs=[env_state, obs_state, done_state, img, action_radio, episode_notice],
    )
    level_dd.change(
        on_task_or_level_change,
        inputs=[task_dd, level_dd],
        outputs=[env_state, obs_state, done_state, img, action_radio, episode_notice],
    )

    # Step / Reset
    btn_step.click(
        on_step,
        inputs=[env_state, obs_state, done_state, action_radio],
        outputs=[img, obs_state, done_state, action_radio, episode_notice],
    )
    btn_reset.click(
        on_reset,
        inputs=[env_state, action_radio],
        outputs=[img, obs_state, done_state, action_radio, episode_notice],
    )

if __name__ == "__main__":
    demo.launch()