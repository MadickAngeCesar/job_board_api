document.addEventListener('DOMContentLoaded', () => {
    const userForm = document.getElementById('userForm');
    const jobForm = document.getElementById('jobForm');
    const applicationForm = document.getElementById('applicationForm');

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
});
