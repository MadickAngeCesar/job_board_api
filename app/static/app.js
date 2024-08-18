document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('register-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const response = await fetch('/users/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: document.getElementById('register-username').value,
                email: document.getElementById('register-email').value,
                password: document.getElementById('register-password').value
            })
        });
        const result = await response.json();
        alert(result.message || result.error);
    });

    document.getElementById('login-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const response = await fetch('/users/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: document.getElementById('login-username').value,
                password: document.getElementById('login-password').value
            })
        });
        const result = await response.json();
        alert(result.message || result.error);
    });

    document.getElementById('create-job-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const response = await fetch('/jobs/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: document.getElementById('job-title').value,
                description: document.getElementById('job-description').value,
                company_name: document.getElementById('company-name').value,
                location: document.getElementById('job-location').value
            })
        });
        const result = await response.json();
        alert(result.message || JSON.stringify(result));
    });

    document.getElementById('submit-application-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('user_id', document.getElementById('application-user-id').value);
        formData.append('job_id', document.getElementById('application-job-id').value);
        formData.append('resume', document.getElementById('resume').files[0]);
        formData.append('cover_letter', document.getElementById('cover-letter').files[0]);

        const response = await fetch('/applications/', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        alert(result.message || JSON.stringify(result));
    });

    document.getElementById('search-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const title = document.getElementById('search-title').value;

        const response = await fetch('/jobs/search?' + new URLSearchParams({
            title
        }));
        const jobs = await response.json();
        
        const searchResults = document.getElementById('search-results');
        searchResults.innerHTML = jobs.length > 0
            ? jobs.map(job => `<li>${job.title} - ${job.company_name} (${job.location})</li>`).join('')
            : '<li>No jobs found</li>';
    });

    async function fetchJobs() {
        const response = await fetch('/jobs/');
        const jobs = await response.json();
        const jobsList = document.getElementById('jobs-list');
        jobsList.innerHTML = jobs.map(job => `<li>${job.title} - ${job.company_name} (${job.location})</li>`).join('');
    }

    fetchJobs();
});
