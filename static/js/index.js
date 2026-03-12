window.HELP_IMPROVE_VIDEOJS = false;

// Task data for carousel
const taskData = [
    {
        title: "Classification (CL)",
        description: "In this task, the agent is required to classify the objects in the grid into different categories based on their attributes. The agent must identify and categorize the objects correctly to complete the task.",
        actions: [
            "pick up the item with label {item_id}",
            "put the item from backpack {backpack_id} into the basket with label {basket_id}"
        ],
        goal: "Place {item_1} in the {color_1} basket and {item_2} in the {color_2} basket."
    },
    {
        title: "Selection (SE)",
        description: "In this task, the agent needs to navigate through the grid environment to reach a specific destination while avoiding obstacles. The agent must plan an efficient path to achieve the goal.",
        actions: [
            "move to position {x}, {y}",
            "pick up the key with label {key_id}",
            "open the door with label {door_id}"
        ],
        goal: "Navigate to the exit while collecting all required keys and avoiding obstacles."
    },
    {
        title: "Maze (MA)",
        description: "This task evaluates the agent's ability to remember and recall information. The agent must observe patterns or sequences and reproduce them accurately after a delay period.",
        actions: [
            "observe the pattern",
            "recall and reproduce the sequence",
            "select item {item_id} in order"
        ],
        goal: "Reproduce the exact sequence of items shown earlier in the correct order."
    },
    {
        title: "Filling (FI)",
        description: "In this task, the agent must create and execute a multi-step plan to achieve a complex goal. This requires reasoning about dependencies between actions and optimizing the sequence of steps.",
        actions: [
            "pick up tool {tool_id}",
            "use tool on object {object_id}",
            "combine items {item_1} and {item_2}"
        ],
        goal: "Complete the construction by using tools and materials in the correct sequence."
    }
];

// Function to update task content
function updateTaskContent(taskIndex) {
    const task = taskData[taskIndex];
    
    // Update title
    document.getElementById('task-title').textContent = task.title;
    
    // Update description
    document.getElementById('task-description').textContent = task.description;
    
    // Update action space
    const actionsElement = document.getElementById('task-actions');
    actionsElement.innerHTML = task.actions.map(action => `<li>${action}</li>`).join('');
    
    // Update goal
    document.getElementById('task-goal').textContent = task.goal;
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
        carousels[0].on('after:show', function(state) {
            // Get the current slide index
            const currentIndex = state.index;
            // Update task content based on current slide
            updateTaskContent(currentIndex);
        });
        
        // Initialize with first task
        updateTaskContent(0);
    }
    
    bulmaSlider.attach();
    
    // Setup video autoplay for carousel
    setupVideoCarouselAutoplay();

})
