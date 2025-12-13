// register.js - handles registration form submission and feedback

const form = document.getElementById('registerForm');
const notice = document.getElementById('notice');
const submitBtn = document.getElementById('submitBtn');
const cancelBtn = document.getElementById('cancelBtn');

// Utility functions to show/hide notices
function showNotice(message, type='success'){
  notice.textContent = message;
  notice.className = 'notice ' + (type === 'error' ? 'error' : 'success');
  notice.style.display = 'block';
}

// Hide notice
function hideNotice(){
  notice.style.display = 'none';
}

// Cancel button redirects to home page
cancelBtn.addEventListener('click', (e)=>{
  window.location.href = '/frontend/static/index.html';
});

// Function to attempt login after registration
async function attemptLogin(username, password){
  try{
    const resp = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({username, password})
    });
    if(!resp.ok){
      return { ok: false, status: resp.status, body: await resp.json().catch(()=>({detail:'Login failed'})) };
    }
    const data = await resp.json();
    return { ok: true, data };
  } catch(err){
    return { ok: false, error: err };
  }
}

// Form submission handler
form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  hideNotice();

  const username = document.getElementById('username').value.trim();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const confirm = document.getElementById('confirm').value;

  if(!username){
    showNotice('Please enter a username', 'error');
    return;
  }
  if(password.length < 4){
    showNotice('Password must be at least 4 characters', 'error');
    return;
  }
  if(password !== confirm){
    showNotice('Password and confirmation do not match', 'error');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = 'Creating...';

  try{
    const resp = await fetch('/api/auth/register', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({username, email, password})
    });

    if(resp.ok){
      // Registration succeeded - attempt auto-login
      showNotice('Account created! Signing you in...', 'success');
      const login = await attemptLogin(username, password);
      if(login.ok){
        // store token and redirect
        try{
          const token = login.data && login.data.access_token ? login.data.access_token : null;
          if(token){
            localStorage.setItem('access_token', token);
            // optional: store token type if needed
            if(login.data.token_type) localStorage.setItem('token_type', login.data.token_type);
          }
        } catch(err){
          // non-fatal storage error
          console.warn('Failed to store token', err);
        }
        // Redirect to game UI (index)
        setTimeout(()=>{
          window.location.href = '/frontend/static/index.html';
        }, 600);
      } else {
        // Auto-login failed - inform the user and offer manual sign-in
        const reason = login.body && login.body.detail ? login.body.detail : (login.error ? String(login.error) : 'Login failed');
        showNotice('Account created but automatic sign-in failed: ' + reason + '. Redirecting to sign-in...', 'error');
        setTimeout(()=>{
          window.location.href = '/frontend/static/index.html';
        }, 1400);
      }

    } else {
      const err = await resp.json().catch(()=>({detail:'Registration failed'}));
      showNotice(err.detail || err.message || 'Registration failed', 'error');
    }
  } catch(err){
    console.error(err);
    showNotice('Network error. Please try again.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Create account';
  }
});
