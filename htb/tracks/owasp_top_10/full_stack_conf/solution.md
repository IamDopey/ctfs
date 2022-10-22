Reading the description of the challenge we know that the vulnerability is in a email form to subscribe to the newsletter.
The title says "xss", maybe is a xss in that form.
This is the javascript code that is on the page:


    const btn = document.getElementById('signup');
    btn.addEventListener('click', e => {
        e.preventDefault();
        fetch('/api/register', {
            method: 'POST',
            body: JSON.stringify({
                email: document.getElementById('email').value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(r => r.json())
        .then(r => {
            if (r.success) {
                document.getElementById('alert').innerHTML = `
                    <div class="alert alert-success">
                        Thank you for signing up to our newsletter
                    </div>
                `;
            }
        });
    });

    // not part of the challenge
    (() => {
        const socket = io();
        socket.on('flag', data => {
            console.log(data.flag);
            alert(data.flag);
        });
    })();

Using <script> alert() </script> as the input we get the flag.

