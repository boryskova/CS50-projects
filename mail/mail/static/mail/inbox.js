document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  console.log(email)
  if ( email ) {
    // Set default values to form inputs
    document.querySelector('#compose-recipients').value = email.sender;

    if ( email.subject.includes('Re:') ) {
      document.querySelector('#compose-subject').value = email.subject;
    } else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }

    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n\t"${email.body}"`;
  } else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  // Send email
  document.querySelector('#compose-form').onsubmit = function(e) {
    e.preventDefault();
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      }) 
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      load_mailbox('sent');
    })
  };
};

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#title').innerHTML = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);

  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails_grid(emails, mailbox);
  });
};

function emails_grid(emails, mailbox) {
  document.querySelector('#emails-view-grid').innerHTML = '';

  for (let i = 0; i < emails.length; i++) {

    // Create grid row for email
    const row = document.createElement('div');
    row.className = 'row';
    row.setAttribute('id', 'emails-view-row');
    row.onclick = () => email_open(emails[i].id);

    // Change row color based on read/unread
    if (emails[i].read === true) {
      row.style.backgroundColor = 'lightgrey';
    } else {
      row.style.backgroundColor = 'white';
    };
    
    // Create columns for email sender
    const sender = document.createElement('div');
    sender.className = 'col-md-3';
    sender.innerHTML = emails[i].sender;
    
    // Create columns for email subject
    const subject = document.createElement('div');
    subject.className = 'col-md-4';
    subject.innerHTML = 'Subject: ' + emails[i].subject;

    if ( mailbox === 'sent' ) {
      // Create columns for email timestamp
      const timestamp = document.createElement('div');
      timestamp.className = 'col-md-5';
      timestamp.innerHTML = emails[i].timestamp;

      row.append(sender, subject, timestamp);
    } else {
      // Create columns for email timestamp
      const timestamp = document.createElement('div');
      timestamp.className = 'col-md-3';
      timestamp.innerHTML = emails[i].timestamp;
      
      // Create columns for archive/unarchive button
      const archive = document.createElement('div');
      archive.className = 'col-md-2';
      archive.setAttribute('id', 'email-archive')
    
      // Create archive/unarchive button
      archive_btn = document.createElement('button');
      archive_btn.className = 'btn btn-sm btn-outline-primary';

      if ( mailbox === 'archive' ) {
        archive_btn.innerHTML = 'Unarchive';
        archive_btn.onclick = (e) => {
          e.stopPropagation();
          unarchive_email(emails[i].id)
        };
      } else {
        archive_btn.innerHTML = 'Archive';
        archive_btn.onclick = (e) => {
          e.stopPropagation();
          archive_email(emails[i].id)
        };
      }

      archive.append(archive_btn);
      row.append(sender, subject, timestamp, archive);
    } 

    // Add row element to document
    document.querySelector('#emails-view-grid').append(row)
  };
};

function email_open(email_id) {

  // Show the email view and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Get the email data
  fetch('/emails/' + email_id)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    // Display the email data
    document.querySelector('#email-from').innerHTML = '<h6>From:</h6>' + email.sender;
    document.querySelector('#email-to').innerHTML = '<h6>To:</h6>' + email.recipients;
    document.querySelector('#email-subject').innerHTML = '<h6>Subject:</h6>' + email.subject;
    document.querySelector('#email-timestamp').innerHTML = '<h6>Timestamp:</h6>' + email.timestamp;
    document.querySelector('#email-body').innerHTML = email.body;

    document.querySelector('#email-reply-btn').onclick = () => compose_email(email);

    // Change read field if email unread
    if ( email.read === false ) {
      read_email(email_id);
    }
  });
};

function archive_email(email_id) {
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify ({
      archived: true
    }) 
  })
  .then( () => load_mailbox('inbox'))
};

function unarchive_email(email_id) {
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify ({
      archived: false
    }) 
  })
  .then( () => load_mailbox('inbox'))
};

function read_email(email_id) {
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify ({
      read: true
    }) 
  });
};
