document.addEventListener('DOMContentLoaded', function() {
    // Select all forms on the admin page
    var forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // If the form has already been submitted, prevent the action
            if (form.classList.contains('is-submitting')) {
                e.preventDefault();
                return false;
            }
            
            // Mark the form as submitting
            form.classList.add('is-submitting');
            
            // Find all submit buttons in this form
            var submitButtons = form.querySelectorAll('input[type="submit"], button[type="submit"]');
            
            submitButtons.forEach(function(button) {
                // Dim the button and disable pointer events
                // (We don't use the 'disabled' attribute here because it strips the button's name/value 
                // from the POST data, which breaks Django's save/continue routing)
                button.style.pointerEvents = 'none';
                button.style.opacity = '0.6';
                
                // Optionally show a saving state
                if (button.tagName === 'INPUT') {
                    button.dataset.originalText = button.value;
                    button.value = 'Saving...';
                } else {
                    button.dataset.originalText = button.textContent;
                    button.textContent = 'Saving...';
                }
            });
        });
    });
});
