document.addEventListener('DOMContentLoaded', () => {

    // generate the csrf token using a function from django website 
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Editing users post
    function update_post() {
        target = this.parentNode;
        this.parentNode.removeChild(this);
        const message = target_div.getElementsByTagName('div')[0].getElementsByTagName('textarea')[0].value;
        target.innerHTML = message;
        const button = document.createElement('input');
        button.setAttribute('class', 'btn btn-outline-secondary btn-sm edit');
        button.setAttribute('type', 'reset');
        button.setAttribute('value', 'edit');
        button.style = "position: absolute; top: 0; right: 0;";
        target.appendChild(button);
        

        // updating post content on the server using fetch
        const data = JSON.stringify({
            message:message,
            msg_id:post_id
        });
        console.log(data);
        fetch('/update', {
                    credentials: 'include',
                    method:'POST',
                    body:data,
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken
            },
        });
        
    };

    const edit_buttons = document.querySelectorAll('.edit')
    Array.from(edit_buttons).forEach(function(element){
        element.addEventListener('click', function(){
            target_div = this.parentNode;
            post_id = this.parentNode.id;
            target = target_div.getElementsByTagName('div')[0];
            const message = target.innerHTML;
            target.innerHTML = '';
            textarea = document.createElement('textarea');
            textarea.setAttribute('row', '3')
            textarea.setAttribute('class', 'form-control form')
            textarea.innerHTML = message.trim();
            button = document.createElement('button');
            button.setAttribute('value', 'save');
            button.setAttribute('type', 'button');
            button.setAttribute('class', 'btn btn-outline-primary btn-sm');
            button.innerHTML = 'Save';
            const token = document.createElement('input');
            token.setAttribute('type', 'hidden');
            token.setAttribute('name', 'csrfmiddlewaretoken')
            token.setAttribute('value',  'nh6JsSSZztBcKN0tfvNKYlD6og7iBoGvAPPL1yA1K1dkwkOI7rbNf3nAroULQbbE')
            target.appendChild(textarea);
            target.appendChild(button);
            target.appendChild(token);
            this.remove();
            button.addEventListener('click', update_post, false);
            

           

            

            
        });
        
    });
    // record  posts likes and edit the database to reflect that
    const like_button = document.querySelectorAll('.like');
    Array.from(like_button).forEach(function (element) {
        element.addEventListener('click', function () {
            if (this.innerHTML.trim().includes('liked')){
                n_likes = parseInt(this.getElementsByTagName('span')[0].innerHTML ) - 1;
                span = document.createElement('span');
                span.innerHTML = n_likes;
                span.setAttribute('class', 'btn btn-outline-primary btn-sm like');
                this.innerHTML = 'like';
                this.appendChild(span);
                console.log(this.parentNode.id);
                data = JSON.stringify({'n_likes':n_likes, 'msg_id':this.parentNode.id, 'action': 'unlike'});
                fetch('/update_post', {
                            credentials: 'include',
                            method: 'POST',
                            body: data,
                        headers : {
                            'Accept' : 'application/json, text/plain, */*',
                            'Content-Type' : 'application/json',
                            'X-CSRFToken' : csrftoken
                        }
                });
            }
            else {
                n_likes = parseInt(this.getElementsByTagName('span')[0].innerHTML) + 1;
                span = document.createElement('span');
                span.innerHTML = n_likes;
                span.setAttribute('class', 'btn btn-outline-primary btn-sm like');
                this.innerHTML = 'liked';
                this.appendChild(span);
                console.log(this.parentNode.id);
                data = JSON.stringify({ 'n_likes': n_likes, 'msg_id': this.parentNode.id, 'action': 'liked' });
                fetch('/update_post', {
                    credentials: 'include',
                    method: 'POST',
                    body: data,
                headers : {
                        'Accept' : 'application/json, text/plain, */*',
                        'Content-Type' : 'application/json',
                        'X-CSRFToken' : csrftoken
                    }
                });
            }
        });

    });
    const follow_button = document.querySelectorAll('.follow');
    //console.log(follow_button)
    Array.from(follow_button).forEach(function(element){
        element.addEventListener('click', function(){
                console.log(this.innerHTML)
                if(this.innerHTML.includes('Following')){
                    this.innerHTML = 'Follow';
                    username = this.parentNode.getElementsByTagName('div')[0].getElementsByTagName('span')[0].getElementsByTagName('a')[0].innerHTML;
                    followers = this.parentNode.getElementsByTagName('div')[0].getElementsByTagName('span')[1]
                    n_followers = parseInt(followers.getElementsByTagName('span')[0].innerHTML)
                    followers.innerHTML = n_followers -1
                    data = JSON.stringify({'username':username, 'action': 'unfollow'});
                    fetch('/update_follow', {
                        credentials: 'include',
                        method: 'POST',
                        body: data,
                    headers: {
                        'Accept': 'application/json, text/plain, */*',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    }
                    });
                }
                else{
                    this.innerHTML = 'Following';
                    username = this.parentNode.getElementsByTagName('div')[0].getElementsByTagName('span')[0].getElementsByTagName('a')[0].innerHTML;
                    followers = this.parentNode.getElementsByTagName('div')[0].getElementsByTagName('span')[1]
                    n_followers = parseInt(followers.getElementsByTagName('span')[0].innerHTML)
                    followers.innerHTML = n_followers + 1
                    data = JSON.stringify({'username': username, 'action': 'following'});
                    fetch('/update_follow', {
                        credentials: 'include',
                        method: 'POST',
                        body:data,
                    headers: {
                        'Accept': 'application/json, text/plain, */*',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    }
                    });
                }
        });
    });
});