  function load_posts(type) {
    document.querySelector('#profile-posts-view').innerHTML = '';
    document.querySelector('#profile-posts-view').style.display = 'block';
    user = document.querySelector('#requestuser1').innerHTML;
    document.querySelector('#requestuser1').style.display = 'none';

    fetch(`posts/${type}`)
    .then(response => response.json())
    .then(posts => {

      posts.forEach(post => {

        const container = document.createElement('div');
        container.className = 'card mb-3';

        const row = document.createElement('div');
          row.className = 'card-body';
          row.setAttribute("id", `postid${post.id}`);
          
          row.innerHTML = `
          <p class="card-text">${post.ppost}</p>
            <p class="card-text"><a href="profile/${post.puser}"><small class="text-muted"><strong>${post.puser}</strong></a>, posted on ${post.pdate} (post-id ${post.id})</small></p>`
            
            if (post.plikes.includes(user)) {
              row.innerHTML += `<div id="numlikes${post.id}" ><i class="fas fa-heart" id="plikebutton${post.id}"></i> ${post.plikesnum}</div>`
            } else { 
              row.innerHTML += `<div id="numlikes${post.id}" ><i class="far fa-heart" id="plikebutton${post.id}"></i> ${post.plikesnum}</div> `
            }    
          ;          

          // Like function
          document.getElementById(`"#numlikes${post.id}"`).addEventListener('click', () => {

            if ( post.plikes.includes(user) ) {
              fetch(`unlikes/${post.id}`, {
                method: 'POST',
                body: JSON.stringify({
                  postid: post.id
                })
              })
              .then(response => response.json())
              .then(json => {
                newplikes = post.plikesnum-1
                document.querySelector(`#numlikes${post.id}`).innerHTML = `<i class="far fa-heart" id="plikebutton${post.id}"></i> ${newplikes}`;
              });
              
              console.log("remove", post.plikes, post.puser, user);
              //location.reload();

            }else{
              fetch(`likes/${post.id}`, {
                method: 'POST',
                body: JSON.stringify({
                  postid: post.id
                })
              })
              .then(response => response.json())
              .then(json => {
                newplikes = post.plikesnum+1
                document.querySelector(`#numlikes${post.id}`).innerHTML = `<i class="fas fa-heart" id="plikebutton${post.id}"></i> ${newplikes}`;
              });
              console.log("add", post.plikes , post.puser, user, post.myplike);
              //location.reload();
            }
            return true;

    
          });


          // edit function
          if ( user == post.puser) {
            row.innerHTML += `<div id="edit${post.id}" style="cursor:hand;"><p class="card-text"><small class="text-muted">Edit</small></p></div>`
            ;
          }   
        ;   

        container.append(row);
        document.querySelector('#profile-posts-view').append(container);
      });
    });
  }
