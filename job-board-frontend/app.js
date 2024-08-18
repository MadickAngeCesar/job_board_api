document.addEventListener('DOMContentLoaded', () => {
    const userForm = document.getElementById('userForm');
    const jobForm = document.getElementById('jobForm');
    const applicationForm = document.getElementById('applicationForm');
    const updateJobForm = document.getElementById('updateJobForm');
    const deleteJobForm = document.getElementById('deleteJobForm');
    const searchForm = document.getElementById('searchForm');
    const searchResults = document.getElementById('searchResults');

    userForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const passwordHash = document.getElementById('passwordHash').value;

        try {
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    email,
                    password_hash: passwordHash
                })
            });
            const data = await response.json();
            alert(data.status);
        } catch (error) {
            alert('Error creating user');
        }
    });

    jobForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const companyName = document.getElementById('companyName').value;
        const location = document.getElementById('location').value;

        try {
            const response = await fetch('/api/jobs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    title,
                    description,
                    company_name: companyName,
                    location
                })
            });
            const data = await response.json();
            alert(data.status);
        } catch (error) {
            alert('Error creating job');
        }
    });

    applicationForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userId = document.getElementById('userId').value;
        const jobId = document.getElementById('jobId').value;
        const resume = document.getElementById('resume').files[0];
        const coverLetter = document.getElementById('coverLetter').files[0];

        const formData = new FormData();
        formData.append('user_id', userId);
        formData.append('job_id', jobId);
        formData.append('resume', resume);
        formData.append('cover_letter', coverLetter);

        try {
            const response = await fetch('/api/applications', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            alert(data.status);
        } catch (error) {
            alert('Error submitting application');
        }
    });

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = document.getElementById('searchQuery').value;

        try {
            const response = await fetch(`/api/jobs/search?query=${encodeURIComponent(query)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            displaySearchResults(data);
        } catch (error) {
            alert('Error searching jobs');
        }
    });

    function displaySearchResults(jobs) {
        searchResults.innerHTML = '';
        if (jobs.length > 0) {
            jobs.forEach(job => {
                const jobElement = document.createElement('div');
                jobElement.classList.add('job-result');
                jobElement.innerHTML = `
                    <h3>${job.title}</h3>
                    <p>${job.description}</p>
                    <p><strong>Company:</strong> ${job.company_name}</p>
                    <p><strong>Location:</strong> ${job.location}</p>
                    <p><strong>Posted:</strong> ${new Date(job.posted_date).toLocaleDateString()}</p>
                `;
                searchResults.appendChild(jobElement);
            });
        } else {
            searchResults.innerHTML = '<p>No jobs found.</p>';
        }
    }
    
    // Handle Job Update
    updateJobForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const jobId = document.getElementById('updateJobId').value;
        const title = document.getElementById('updateJobTitle').value;
        const description = document.getElementById('updateJobDescription').value;
        const companyName = document.getElementById('updateJobCompany').value;
        const location = document.getElementById('updateJobLocation').value;

        try {
            const response = await fetch(`/api/jobs/${jobId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getAuthToken()}`
                },
                body: JSON.stringify({
                    title,
                    description,
                    company_name: companyName,
                    location
                })
            });
            const data = await response.json();
            alert(data.status);
        } catch (error) {
            alert('Error updating job');
        }
    });

    // Handle Job Deletion
    deleteJobForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const jobId = document.getElementById('deleteJobId').value;

        try {
            const response = await fetch(`/api/jobs/${jobId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`
                }
            });
            const data = await response.json();
            alert(data.status);
        } catch (error) {
            alert('Error deleting job');
        }
    });
});
