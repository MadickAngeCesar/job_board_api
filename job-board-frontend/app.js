document.getElementById('application-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('user_id', document.getElementById('user_id').value);
    formData.append('job_id', document.getElementById('job_id').value);
    formData.append('resume', document.getElementById('resume').files[0]);
    formData.append('cover_letter', document.getElementById('cover_letter').files[0]);

    try {
        const response = await fetch('http://localhost:5000/api/job/apply', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('application-result').innerText = 'Application submitted successfully!';
        } else {
            document.getElementById('application-result').innerText = `Error: ${result.error}`;
        }
    } catch (error) {
        console.error('Error submitting application:', error);
        document.getElementById('application-result').innerText = 'Error submitting application.';
    }
});

document.getElementById('status-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const userId = document.getElementById('status_user_id').value;
    const jobId = document.getElementById('status_job_id').value;

    try {
        const response = await fetch(`http://localhost:5000/api/application/status?user_id=${userId}&job_id=${jobId}`);

        const result = await response.json();

        if (response.ok) {
            document.getElementById('status-result').innerText = `Application Status: ${result.status}`;
        } else {
            document.getElementById('status-result').innerText = `Error: ${result.error}`;
        }
    } catch (error) {
        console.error('Error checking status:', error);
        document.getElementById('status-result').innerText = 'Error checking status.';
    }
});

document.getElementById('create-job-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const company_name = document.getElementById('company_name').value;
    const location = document.getElementById('location').value;

    fetch('/api/jobs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, description, company_name, location })
    }).then(response => response.json())
      .then(data => {
          loadJobs();
      });
});

function loadJobs() {
    fetch('/api/jobs')
        .then(response => response.json())
        .then(data => {
            const jobList = document.getElementById('job-list');
            jobList.innerHTML = '';
            data.forEach(job => {
                const jobItem = document.createElement('div');
                jobItem.className = 'job-item';
                jobItem.innerHTML = `
                    <h3>${job.title}</h3>
                    <p>${job.description}</p>
                    <p><strong>Company:</strong> ${job.company_name}</p>
                    <p><strong>Location:</strong> ${job.location}</p>
                    <p><strong>Posted on:</strong> ${new Date(job.posted_date).toLocaleDateString()}</p>
                `;
                jobList.appendChild(jobItem);
            });
        });
}

window.onload = loadJobs;
