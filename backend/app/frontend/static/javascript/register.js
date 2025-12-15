// register.js - handles registration form submission and feedback

// Get form elements
const form = document.getElementById('registerForm');
const notice = document.getElementById('notice');
const submitBtn = document.getElementById('submitBtn');
const cancelBtn = document.getElementById('cancelBtn');

// Utility functions to show/hide notices
function showNotice(message, type='success'){
 // type can be 'success' or 'error'
  notice.textContent = message;
  notice.className = 'notice ' + (type === 'error' ? 'error' : 'success');
  notice.style.display = 'block';
}

// Hide notice
function hideNotice(){
// Clear and hide notice
  notice.style.display = 'none';
}

// Cancel button redirects to home page
cancelBtn.addEventListener('click', (e)=>{
// Redirect to home page
  window.location.href = '/frontend/static/index.html';
});

// Function to attempt login after registration
async function attemptLogin(username, password){
  try{
  // Send login request
    const resp = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({username, password})
    });
    // Check response
    if(!resp.ok){
      return { ok: false, status: resp.status, body: await resp.json().catch(()=>({detail:'Login failed'})) };
    }
     // Parse response data
    const data = await resp.json();
    // Return success with data
    return { ok: true, data };
  } catch(err){
    // Network or other error
    return { ok: false, error: err };
  }
}

// Form submission handler
form.addEventListener('submit', async (e)=>{
// Prevent default form submission
  e.preventDefault();
  // Clear previous notices
  hideNotice();

    // Get form values
  const username = document.getElementById('username').value.trim();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const confirm = document.getElementById('confirm').value;

    // Basic validation
  if(!username){
    showNotice('Please enter a username', 'error');
    return;
  }
  // Simple email format check
  if(password.length < 4){
    showNotice('Password must be at least 4 characters', 'error');
    return;
  }
  // Check password confirmation
  if(password !== confirm){
    showNotice('Password and confirmation do not match', 'error');
    return;
  }

    // Disable submit button to prevent multiple submissions
  submitBtn.disabled = true;
  submitBtn.textContent = 'Creating...';

 // Send registration request
  try{
  // Call registration API
    const resp = await fetch('/api/auth/register', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({username, email, password})
    });
    // Check response
    if(resp.ok){
      // Registration succeeded - attempt auto-login
      showNotice('Account created! Signing you in...', 'success');
      // Attempt login
      const login = await attemptLogin(username, password);
      // Check login result
      if(login.ok){
        // store token and redirect
        try{
        // Store access token in localStorage
          const token = login.data && login.data.access_token ? login.data.access_token : null;
          if(token){
          // Store token
            localStorage.setItem('access_token', token);
            // store token type
            if(login.data.token_type) localStorage.setItem('token_type', login.data.token_type);
          }
        } catch(err){
          // non-fatal storage error
          console.warn('Failed to store token', err);
        }
        // Redirect to game UI (index)
        setTimeout(()=>{
        // Redirect to main page
          window.location.href = '/frontend/static/index.html';
        }, 600);
      } else {
        // Auto-login failed - inform the user and offer manual sign-in
        const reason = login.body && login.body.detail ? login.body.detail : (login.error ? String(login.error) : 'Login failed');
        // Show notice and redirect to sign-in page
        showNotice('Account created but automatic sign-in failed: ' + reason + '. Redirecting to sign-in...', 'error');
        // Redirect to main page after a delay
        setTimeout(()=>{
        // Redirect to main page
          window.location.href = '/frontend/static/index.html';
        }, 1400);
      }

    } else {
        // Registration failed - show error message
      const err = await resp.json().catch(()=>({detail:'Registration failed'}));
      // Show error notice
      showNotice(err.detail || err.message || 'Registration failed', 'error');
    }
  } catch(err){
  // Network or other error
    console.error(err);
    // Show error notice
    showNotice('Network error. Please try again.', 'error');
  } finally {
    // Re-enable submit button
    submitBtn.disabled = false;
    submitBtn.textContent = 'Create account';
  }
});
