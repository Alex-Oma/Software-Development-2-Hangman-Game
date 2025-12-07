// login.js - handle existing user sign-in and token storage

const form = document.getElementById('loginForm');
const notice = document.getElementById('notice');
const submitBtn = document.getElementById('submitBtn');

function showNotice(message, type='error'){
  notice.textContent = message;
  notice.className = 'notice ' + (type === 'error' ? 'error' : 'success');
  notice.style.display = 'block';
}
function hideNotice(){ notice.style.display = 'none'; }

form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  hideNotice();
  submitBtn.disabled = true;
  submitBtn.textContent = 'Signing in...';

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;

  if(!username || !password){
    showNotice('Please enter username and password', 'error');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign in';
    return;
  }

  try{
    const resp = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({username, password})
    });

    if(!resp.ok){
      const err = await resp.json().catch(()=>({detail:'Sign-in failed'}));
      showNotice(err.detail || 'Sign-in failed', 'error');
      return;
    }

    const data = await resp.json();
    const token = data && data.access_token ? data.access_token : null;
    if(token){
      try{
        localStorage.setItem('access_token', token);
        if(data.token_type) localStorage.setItem('token_type', data.token_type);
      } catch(err){
        console.warn('Failed to store token', err);
      }
      // Redirect to game UI
      window.location.href = '/frontend/static/index.html';
    } else {
      showNotice('No token received', 'error');
    }
  } catch(err){
    console.error(err);
    showNotice('Network or server error. Try again later', 'error');
  } finally{
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign in';
  }
});

