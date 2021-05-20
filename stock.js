document.addEventListener('DOMContentLoaded', function load() {

  

  document.querySelector('#searchbutton').addEventListener('click', function search() {
    let getsearchword = document.querySelector('#searchword').value;
    let getsearchby = document.querySelector('#searchby').value;
    document.querySelector('#searchwordstore').innerHTML = `${getsearchword}`;
    document.querySelector('#searchbystore').innerHTML = `${getsearchby}`;
    const searchword = document.querySelector('#searchwordstore').innerHTML
    const searchby = document.querySelector('#searchbystore').innerHTML
    document.querySelector('#message').innerHTML = `Search result for ${searchword}`;
    load_items(1, searchby, searchword); pagi(1, searchby, searchword); 
    return false;
  })

  function pagi(page, key, word) {
    var page = page
    var searchby = key
    var searchword = word
    fetch(`page/`, {
      method: 'POST',
      body: JSON.stringify({
        page: page,
        searchword: searchword,
        searchby: searchby
      })
    })
    .then(response => response.json())
    .then(link => { 

      var text = "";
      for (var pages = 1; pages <= link.plen; pages++) {
        var idpage = "#b"+pages
        text += "<li class='page-item' style='float: left; cursor:pointer;' id='" + (idpage) + "'><span class='page-link'>" + pages + "</span></li>";
        
      }
      document.querySelector('#pagebutton').innerHTML = text;

      var funcs = [];

      function createFunc(i) {
        return function() {
          
          if( i == page) {
            document.getElementById('#b'+i).className = "page-item active";
            document.getElementById('#b'+i).style.cursor = "default";
          } else {
            document.getElementById('#b'+i).addEventListener('click', function() {load_items(i); pagi(i); })
          }

        }.call(this);
      }

      for (var i = 1; i <= link.plen; i++) {  
        funcs[i] = createFunc(i);    
      } 


      document.querySelector('#nextbutton').style.display = 'block';
      document.querySelector('#prebutton').style.display = 'block';


      if (page == 1) {
        document.querySelector('#prebutton').style.display = 'none';
      } 
      if (page == link.plen) {
        document.querySelector('#nextbutton').style.display = 'none';
      }

      document.querySelector('#nextbutton').addEventListener('click', function() {load_items(page+1); pagi(page+1); })
      document.querySelector('#prebutton').addEventListener('click', function() {load_items(page-1); pagi(page-1); })
    
    return false;
    })
  }




  function load_items(page, key, word) {
    var page = page
    var searchby = key
    var searchword = word
    document.querySelector('#resulttable').innerHTML = "";
    document.querySelector('#resulttable').innerHTML += `<thead class="thead-dark">
    <tr>
        <th>Code</th>
        <th>Picture</th>
        <th>Name</th>
        <th>Color</th>
        <th>Shop</th>
        <th>Factory</th>
    </tr>
</thead>`;

    fetch(`stocks/`, {
      method: 'POST',
      body: JSON.stringify({
        page: page,
        searchword: searchword,
        searchby: searchby
      })
    })
    .then(response => response.json())
    .then(items => {

      items.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `        
        <td>${item.code}</td>
        <td>${item.url}</td>
        <td>${item.nameen}</td>
        <td>${item.coloren}</td>
        <td>${item.shop}</td>
        <td>${item.factory}</td>`;
        document.querySelector('#resulttable').append(row);
      });
    })
    return false;
  }

  




})