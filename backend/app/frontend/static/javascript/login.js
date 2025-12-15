// login.js - handle existing user sign-in and token storage

// Get elements
const form = document.getElementById('loginForm');
const notice = document.getElementById('notice');
const submitBtn = document.getElementById('submitBtn');

// Show or hide notice
function showNotice(message, type='error'){
// type: 'error' or 'success'
  notice.textContent = message;
  notice.className = 'notice ' + (type === 'error' ? 'error' : 'success');
  notice.style.display = 'block';
}
// Hide notice
function hideNotice(){ notice.style.display = 'none'; }

// Handle form submission
form.addEventListener('submit', async (e)=>{
// Prevent default form submission
  e.preventDefault();
  // Clear previous notice
  hideNotice();
  // Disable submit button to prevent multiple submissions
  submitBtn.disabled = true;
  // Change button text to indicate processing
  submitBtn.textContent = 'Signing in...';

// Get form values
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;

// Basic validation
  if(!username || !password){
  // Show error notice
    showNotice('Please enter username and password', 'error');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign in';
    return;
  }
// Send login request
  try{
  // Make POST request to login API
    const resp = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({username, password})
    });
    // Check response status
    if(!resp.ok){
    // Show error notice
      const err = await resp.json().catch(()=>({detail:'Sign-in failed'}));
      showNotice(err.detail || 'Sign-in failed', 'error');
      return;
    }
    // Parse response JSON
    const data = await resp.json();
    const token = data && data.access_token ? data.access_token : null;
    // Store token in localStorage
    if(token){
      try{
      // Save token and token type
        localStorage.setItem('access_token', token);
        if(data.token_type) localStorage.setItem('token_type', data.token_type);
      } catch(err){
      // Storage error
        console.warn('Failed to store token', err);
      }
      // Redirect to game UI
      window.location.href = '/frontend/static/game.html';
    } else {
    // No token received
      showNotice('No token received', 'error');
    }
  } catch(err){
  // Network or other error
    console.error(err);
    showNotice('Network or server error. Try again later', 'error');
  } finally{
  // Re-enable submit button
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign in';
  }
});
