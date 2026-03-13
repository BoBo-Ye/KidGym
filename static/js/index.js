window.HELP_IMPROVE_VIDEOJS = false;

// Task data for carousel
const taskData = [
    {
        title: "Classification (CL)",
        description: "In CL task, the agent is required to place each item into its designated container based on specific instructions. It is designed to evaluate the MLLM's Execution ability, which involves translating an understanding of goals into effective actions. The agent's performance in this task measures its accuracy in following instructions within a structured environment.",
        goal: "Place hamburger in the green basket and sushi in the blue basket."
    },
    {
        title: "Selection (SE)",
        description: "In SE task, several random items will appear in the left hint bar at first. Once the task starts, these items will be hidden, and the agent need to select the items that appeared in the hint bar before. This task evaluates the MLLM's Memory capability by requiring it to remember and recall the items previously shown.",
        goal: "In the first image, an item will be shown on the left hint bar that you need to remember. In the following images, several random items will be generated in the scene, and you need to select the ones you recall."
    },
    {
        title: "Sorting (SO)",
        description: "In SO task, the agent is presented with a rule that may contradict real-world knowledge. The agent is expected to correctly rank the animals based on the given rule. This task evaluates the MLLM's Learning abilities, as it requires the agent to comprehend a novel rule that may conflict with its prior knowledge.",
        goal: "In this world, the slower the animal is, the heavier it is. Rank the animal in the backpack from heaviest to lightest in position I, II, III."
    },
    {
        title: "Maze (MA)",
        description: "In MA task, the agent must obtain the diamond in a maze with several locked doors. The agent needs to collect the corresponding colored keys to unlock these doors. This task primarily evaluates the MLLM's Planning ability, as the agent should carefully devise a strategy to reach the diamond with the fewest steps.",
        goal: "There is a diamond shown in the scene, and you need to obtain the diamond. When your path is blocked by a door, you can use a key of the same color to unlock it. Note: You must pick up the key first before you can use it to unlock doors."
    },
    {
        title: "Filling (FI)",
        description: "In FI task, the agent will be presented with an image in which a quarter section has been removed. Then it needs to restore the image by selecting the correct missing piece from a set of distractors in the backpack. This task primarily evaluates the MLLM's Perception Reasoning ability, as it requires the agent to develop a holistic understanding of the image and infer the missing part.",
        goal: "There is a target item shown on the left hint bar. You need to fill the correct pieces from the backpack to complete the missing parts of the frame in the scene, ensuring they match and align with the target item."
    },
    {
        title: "Puzzle (PU)",
        description: "In PU task, a target image composed of 4 puzzle pieces is displayed in the hint and the agent needs to assemble the scattered puzzle pieces from its backpack to reconstruct the target. This task primarily evaluates the MLLM's Perception Reasoning in abstract visual mode, as it requires the agent to grasp the image's overall structure, which cannot be easily conveyed through language.",
        goal: "There is a target item shown on the left hint bar. You need to fill the correct pieces from the backpack to complete the missing parts of the frame in the scene, ensuring they match and align with the target item."
    },
    {
        title: "Placement (PL)",
        description: "In PL task, the agent is required to place the item in the opposite position based on the given goal. This task primarily evaluates the MLLM's abilities in Learning and Perception Reasoning, as it necessitates an understanding of placement rules and the awareness of spatial orientation.",
        goal: "A direction will be provided: northeast. Determine its opposite direction, and then place grape in the corresponding location around cherry."
    },
    {
        title: "Counting (CO)",
        description: "In CO task, the scene contains several piles of items, with quantities ranging from 1 to 3. At the start of the task, the agent is given a target number and then it must collect exactly that number of items. This task primarily evaluates the MLLM's Perception Reasoning and Planning abilities, focusing on the agent's awareness of item quantities and its strategic decision-making regarding how many items to collect at single time.",
        goal: "Collect 6 eggs from the scene and place them in the backpack. Make sure you have gathered exactly this amount, no more and no less. You should be aware that there may be 1 to 3 items of different quantities in one grid."
    },
    {
        title: "Decode Maze (DMA)",
        description: "This task follows the same rules as the “Maze”, with an added challenge. The agent can no longer use a same-colored key to open a door. Instead, it must learn the “key-door” correspondence shown in the hint bar. This task evaluates the MLLM's Learning and Planning abilities, requiring the agent to leverage the hint information to make correct choices and formulate a series of plans to obtain the diamond as few steps as possible.",
        goal: "There is a diamond in the scene, and your goal is to obtain it. Some paths are blocked by doors, and the key required to unlock each door color is shown in the left hint panel. You must consult the hint bar and use the specified key to open the corresponding door."
    },
    {
        title: "Memory Maze (MMA)",
        description: "This task follows the same rules as the “Maze”, with an added challenge. Before the task begins, the agent is shown the location of the diamond, but once the task starts, the diamond in the scene will be hidden and several treasure chests will appear. To succeed, the agent must correctly open the chest containing the diamond. This task primarily assesses the MLLM's Memory and Planning abilities, as the agent must recall the diamond's location and devise an effective strategy to retrieve it.",
        goal: "In the first image, a diamond will be shown in the scene that you need to remember its location. In the following images, the diamond will not be shown and several treasure boxes will be generated in the scene. You must choose to open the treasure box located at the diamond's original position to obtain the diamond."
    },

    {
        title: "Memory Decode (MDE)",
        description: "In MDE task, the agent is provided with a hint bar, which contains a certain number of association rules between different items and it must remember the item relationships because these will be hidden once the task starts. This task evaluates the MLLM's abilities in Memory and Learning, as it requires the agent to retain and utilize the information from the hint bar to make accurate selections.",
        goal: "In the first image, arrow-connected items with one-to-one correspondences will be shown on the left margin that you need to remember. In the following images, the correspondences will not be shown, and a target item will be generated in the black box in the upper left corner. You need to select the correct corresponding item for the target based on the pairing you remembered in the first imag."
    },
    {
        title: "Memory Filling (MFI)",
        description: "This task follows the same rules as “Filling”, with an added challenge. The agent must additionally remember the target, which will disappear once the task starts. This task primarily evaluates the MLLM's abilities in Perception Reasoning and Memory, as it necessitates recognizing the overall image and recalling specific details to identify the correct piece.",
        goal: "In the first image, a target item will be shown on the left margin that you need to remember. In the following images, the target item will not be shown. You need to fill the correct pieces from the backpack to complete the missing parts of the frame in the scene, ensuring they match and align with the target item. "
    },
];

// Function to update task content
function updateTaskContent(taskIndex) {
    // Handle loop: ensure index is within valid range [0, taskData.length-1]
    const validIndex = ((taskIndex % taskData.length) + taskData.length) % taskData.length;
    const task = taskData[validIndex];
    
    if (!task) {
        console.error('Task not found for index:', taskIndex, 'valid index:', validIndex);
        return;
    }
    
    // Update title
    const titleElement = document.getElementById('task-title');
    if (titleElement) {
        titleElement.textContent = task.title;
    }
    
    // Update description
    const descriptionElement = document.getElementById('task-description');
    if (descriptionElement) {
        descriptionElement.textContent = task.description;
    }
    
    // Update goal
    const goalElement = document.getElementById('task-goal');
    if (goalElement) {
        goalElement.innerHTML = `<li>${task.goal}</li>`;
    }
}


// More Works Dropdown Functionality
function toggleMoreWorks() {
    const dropdown = document.getElementById('moreWorksDropdown');
    const button = document.querySelector('.more-works-btn');
    
    if (dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
        button.classList.remove('active');
    } else {
        dropdown.classList.add('show');
        button.classList.add('active');
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const container = document.querySelector('.more-works-container');
    const dropdown = document.getElementById('moreWorksDropdown');
    const button = document.querySelector('.more-works-btn');
    
    if (container && !container.contains(event.target)) {
        dropdown.classList.remove('show');
        button.classList.remove('active');
    }
});

// Close dropdown on escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const dropdown = document.getElementById('moreWorksDropdown');
        const button = document.querySelector('.more-works-btn');
        dropdown.classList.remove('show');
        button.classList.remove('active');
    }
});

// Copy BibTeX to clipboard
function copyBibTeX() {
    const bibtexElement = document.getElementById('bibtex-code');
    const button = document.querySelector('.copy-bibtex-btn');
    const copyText = button.querySelector('.copy-text');
    
    if (bibtexElement) {
        navigator.clipboard.writeText(bibtexElement.textContent).then(function() {
            // Success feedback
            button.classList.add('copied');
            copyText.textContent = 'Cop';
            
            setTimeout(function() {
                button.classList.remove('copied');
                copyText.textContent = 'Copy';
            }, 2000);
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = bibtexElement.textContent;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            button.classList.add('copied');
            copyText.textContent = 'Cop';
            setTimeout(function() {
                button.classList.remove('copied');
                copyText.textContent = 'Copy';
            }, 2000);
        });
    }
}

// Scroll to top functionality
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show/hide scroll to top button
window.addEventListener('scroll', function() {
    const scrollButton = document.querySelector('.scroll-to-top');
    if (window.pageYOffset > 300) {
        scrollButton.classList.add('visible');
    } else {
        scrollButton.classList.remove('visible');
    }
});

// Video carousel autoplay when in view
function setupVideoCarouselAutoplay() {
    const carouselVideos = document.querySelectorAll('.results-carousel video');
    
    if (carouselVideos.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const video = entry.target;
            if (entry.isIntersecting) {
                // Video is in view, play it
                video.play().catch(e => {
                    // Autoplay failed, probably due to browser policy
                    console.log('Autoplay prevented:', e);
                });
            } else {
                // Video is out of view, pause it
                video.pause();
            }
        });
    }, {
        threshold: 0.5 // Trigger when 50% of the video is visible
    });
    
    carouselVideos.forEach(video => {
        observer.observe(video);
    });
}

$(document).ready(function() {
    // Check for click events on the navbar burger icon

    var options = {
		slidesToScroll: 1,
		slidesToShow: 1,
		loop: true,
		infinite: true,
		autoplay: false,
		autoplaySpeed: 5000,
		pagination: false,
    }

	// Initialize all div with carousel class
    var carousels = bulmaCarousel.attach('.carousel', options);
	
    // Add event listener for carousel slide change
    if (carousels.length > 0) {
        const resultsCarousel = carousels.find(c => c.element && c.element.id === 'results-carousel');
        
        if (resultsCarousel) {
            // Only use before:show event with state.next
            // This ensures text updates to the correct slide that will be shown
            resultsCarousel.on('before:show', function(state) {
                if (state && typeof state.next !== 'undefined') {
                    const nextIndex = state.next;
                    console.log('Carousel switching to index:', nextIndex);
                    updateTaskContent(nextIndex);
                }
            });
            
            // Initialize with first task
            updateTaskContent(0);
        }
    }
    
    bulmaSlider.attach();
    
    // Setup video autoplay for carousel
    setupVideoCarouselAutoplay();

})
