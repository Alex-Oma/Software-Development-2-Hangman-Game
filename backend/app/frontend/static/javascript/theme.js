// theme.js - shared theme handling for light/dark mode across pages
(function(){
  const ROOT_ID = 'app';
  const TOGGLE_ID = 'toggleTheme';
  const STORAGE_KEY = 'theme';

    // Utility functions
  function getAppEl(){
    return document.getElementById(ROOT_ID);
  }

    // Get the theme toggle button element
  function getToggleEl(){
    return document.getElementById(TOGGLE_ID);
  }

    // Get the root element for theme class application
  function getThemeRoot(){
    return document.documentElement; // <html>
  }

// Apply the given theme class to the root element
  function applyThemeClass(theme){
  // theme should be 'light' or 'dark'
    const root = getThemeRoot();
    if(!root) return;
    if(theme === 'dark'){
      root.classList.remove('theme-light');
      root.classList.add('theme-dark');
    } else if(theme === 'light'){
      root.classList.remove('theme-dark');
      root.classList.add('theme-light');
    }

    // Also update the #app element classes to avoid conflicts when pages
    // pre-set theme classes on the app container.
    const app = getAppEl();
    if(app){
    // remove both and add the correct one
      app.classList.remove('theme-light','theme-dark');
      app.classList.add(theme === 'dark' ? 'theme-dark' : 'theme-light');
    }

    // update aria-pressed on toggle if present
    const toggle = getToggleEl();
    if(toggle){
    // set aria-pressed based on current theme
      const pressed = theme === 'dark';
      toggle.setAttribute('aria-pressed', pressed ? 'true' : 'false');
    }
  }

    // Initialize theme based on stored preference or system setting
  function initTheme(){
    const root = getThemeRoot();
    if(!root) return;
    // check localStorage first
    const stored = localStorage.getItem(STORAGE_KEY);
    // validate stored value
    if(stored === 'dark' || stored === 'light'){
    // apply stored preference
      applyThemeClass(stored);
      return;
    }
    // fallback to system preference
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    // apply system preference
    applyThemeClass(prefersDark ? 'dark' : 'light');
  }

// Create the contents of the toggle button
  function createToggleContents(button){
    if(!button) return;
    // if already decorated, skip
    if(button.querySelector('.theme-toggle-icon')) return;

    // inline SVGs for sun and moon (kept simple)
    const sunSvg = `<svg class="sun" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.5" fill="none"/><g stroke="currentColor" stroke-width="1.4"><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M4.93 19.07l1.41-1.41"/><path d="M17.66 6.34l1.41-1.41"/></g></svg>`;
    const moonSvg = `<svg class="moon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke="currentColor" stroke-width="1.4" fill="none"/></svg>`;

    // build wrapper
    const wrapper = document.createElement('span');
    wrapper.className = 'toggle-icon-wrapper';
    // create an icon-only button (SVGs are aria-hidden) and rely on the button's aria-label for accessibility
    wrapper.innerHTML = `<span class="theme-toggle-icon">${sunSvg}${moonSvg}</span>`;

    // clear existing content but preserve accessible name if present
    const existingText = button.getAttribute('aria-label') || button.textContent.trim();
    // set accessible name if not already present
    if(!button.getAttribute('aria-label')){
      button.setAttribute('aria-label', existingText || 'Toggle theme');
    }
    // replace content
    button.innerHTML = '';
    button.appendChild(wrapper);
  }

// Toggle between light and dark themes
  function toggleTheme(){
  // determine current theme
    const root = getThemeRoot();
    if(!root) return;
    // check current theme
    const isLight = root.classList.contains('theme-light');
    const next = isLight ? 'dark' : 'light';
    // apply next theme
    applyThemeClass(next);
    // store preference
    localStorage.setItem(STORAGE_KEY, next);
  }

// Handle click events on the toggle button
  function handleToggleClick(event){
  // check if the click was on or within the toggle button
    const target = event.target.closest ? event.target.closest('#' + TOGGLE_ID) : null;
    // if found, toggle theme
    if(target){
      // ensure toggle contents exist
      createToggleContents(target);
      // toggle theme
      toggleTheme();
      // maintain focus on the button
      target.focus();
    }
  }

// Attach event handlers for the toggle button
  function attachToggleHandler(){
    // Decorate the button if present now
    const btn = getToggleEl();
    // create contents
    if(btn) createToggleContents(btn);

    // Ensure clicks anywhere on the document that hit the toggle are handled
    // This guards against the button being replaced by other scripts.
    document.addEventListener('click', handleToggleClick);

    // Keyboard activation: delegate to keydown on document and check target
    document.addEventListener('keydown', function(e){
    // check if active element is the toggle button
      const active = document.activeElement;
      if(!active) return;
      // check for Enter or Space key
      if(active.id === TOGGLE_ID && (e.key === 'Enter' || e.key === ' ')){
      // prevent scrolling for Space
        e.preventDefault();
        // ensure contents and toggle
        createToggleContents(active);
        // toggle theme
        toggleTheme();
      }
    });

    // set initial aria-pressed if button exists
    const currentBtn = getToggleEl();
    // update its state
    if(currentBtn){
    // set aria-pressed based on current theme
      const root = getThemeRoot();
      // determine if dark mode is active
      const pressed = root && root.classList.contains('theme-dark');
      // set attribute
      currentBtn.setAttribute('aria-pressed', pressed ? 'true' : 'false');
      currentBtn.setAttribute('role','button');
      // ensure it's focusable
      if(!currentBtn.hasAttribute('tabindex')) currentBtn.setAttribute('tabindex','0');
    }
  }

  // expose minimal API for pages that want to call programmatically
  window.hangmanTheme = {
    initTheme,
    toggleTheme,
    applyThemeClass,
  };

  // auto-init when script loads
  if(document.readyState === 'loading'){
  // wait for DOMContentLoaded
    document.addEventListener('DOMContentLoaded', ()=>{ initTheme(); attachToggleHandler(); });
  } else {
    // DOM is ready so initialize now
    initTheme(); attachToggleHandler();
  }
})();
