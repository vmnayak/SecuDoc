// Sidebar toggle
document.getElementById('menu-toggle').addEventListener('click', function () {
  document.getElementById('sidebar').classList.toggle('collapsed');
});

document.addEventListener('DOMContentLoaded', function () {
  const profileIcon = document.getElementById('profile-icon');
  const profilePanel = document.getElementById('profile-panel');
  const closeProfile = document.getElementById('close-profile-panel');
  const overlay = document.getElementById('popup-overlay');

  const changePasswordBtn = document.getElementById('open-password-panel');
  const changePasswordPanel = document.getElementById('change-password-panel');
  const closePasswordPanel = document.getElementById('close-password-panel');

  // Show profile panel
  profileIcon.addEventListener('click', function () {
    profilePanel.classList.add('show');
    overlay.style.display = 'block';
  });

  // Close profile panel
  closeProfile.addEventListener('click', function () {
    profilePanel.classList.remove('show');
    overlay.style.display = 'none';
  });

  // Open change password panel
  changePasswordBtn.addEventListener('click', function () {
    profilePanel.classList.remove('show');
    changePasswordPanel.classList.add('show');
    overlay.style.display = 'block';
  });

  // Close change password panel
  closePasswordPanel.addEventListener('click', function () {
    changePasswordPanel.classList.remove('show');
    overlay.style.display = 'none';
  });

  // Click outside to close all popups
  overlay.addEventListener('click', function () {
    profilePanel.classList.remove('show');
    changePasswordPanel.classList.remove('show');
    overlay.style.display = 'none';
  });

  // Submit password form
  document.getElementById('change-password-form').addEventListener('submit', function (e) {
    e.preventDefault();
    // Here you can add validation / API call
    alert('Password updated successfully!');
    changePasswordPanel.classList.remove('show');
    overlay.style.display = 'none';
  });
});
