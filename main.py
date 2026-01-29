import argparse

from src import Evaluation
from tasks import TASK_NAMES


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "KidGym: A 2D Grid-Based Reasoning Benchmark for MLLMs")
    parser.add_argument("--task", type=str, default= "CL_L1", help="Task Name", choices = TASK_NAMES)
    args = parser.parse_args()

    evaluation = Evaluation(args.task)
    evaluation.run()

