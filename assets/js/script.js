
window.onload = function() {
  document.querySelectorAll('pre.sourceCode')
    .forEach(
      function(item) {
        item.addEventListener('click',
          function(elem)
          { text = item.textContent;
            navigator.clipboard.writeText(text)
              .then( function() {
                item.classList.add('copied')
  	      setTimeout(function(){
  		item.classList.remove('copied')
  		}, 2000)
              })
              .catch(err => {
                alert('Error in copying text: ', err);
              });
          })
      }
    )
}
