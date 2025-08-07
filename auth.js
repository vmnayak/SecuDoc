document.addEventListener('DOMContentLoaded', function () {
    const goToSignup = document.getElementById('goToSignup');
    const goToLogin = document.getElementById('goToLogin');

    /* --- Page Flip Animation --- */
    if (goToSignup) {
        goToSignup.addEventListener('click', (e) => {
            e.preventDefault();
            const box = document.querySelector('.auth-container');
            box.classList.add('flip-out');
            setTimeout(() => { window.location.href = 'signup.html'; }, 600);
        });
    }
    if (goToLogin) {
        goToLogin.addEventListener('click', (e) => {
            e.preventDefault();
            const box = document.querySelector('.auth-container');
            box.classList.add('flip-out');
            setTimeout(() => { window.location.href = 'login.html'; }, 600);
        });
    }

    /* --- Password Eye Toggle --- */
    document.querySelectorAll('.password-toggle').forEach(icon => {
        icon.addEventListener('click', () => {
            const targetId = icon.getAttribute('data-target');
            const input = document.getElementById(targetId);
            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            } else {
                input.type = "password";
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            }
        });
    });

    /* --- Phone Number Restriction --- */
    const phoneInput = document.getElementById('signupPhone');
    if (phoneInput) {
        phoneInput.addEventListener('input', () => {
            // Allow only digits and limit to 10
            phoneInput.value = phoneInput.value.replace(/[^0-9]/g, '').slice(0, 10);
        });
    }

    /* --- Live Confirm Password Check with length condition --- */
    const password = document.getElementById('signupPassword');
    const confirmPassword = document.getElementById('signupConfirmPassword');
    const passwordError = document.getElementById('passwordError');

    if (password && confirmPassword && passwordError) {
        confirmPassword.addEventListener('input', () => {
            const passLen = password.value.length;
            const confirmLen = confirmPassword.value.length;
            if (confirmLen >= passLen && password.value !== confirmPassword.value) {
                passwordError.style.display = "block";
            } else {
                passwordError.style.display = "none";
            }
        });

        password.addEventListener('input', () => {
            const passLen = password.value.length;
            const confirmLen = confirmPassword.value.length;
            if (confirmLen >= passLen && password.value !== confirmPassword.value) {
                passwordError.style.display = "block";
            } else {
                passwordError.style.display = "none";
            }
        });
    }
});
