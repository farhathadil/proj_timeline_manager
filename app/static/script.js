document.addEventListener('click', function(e){
  const t = e.target;
  if (t.classList && t.classList.contains('marker')){
    const desc = t.getAttribute('data-desc') || '';
    alert(desc);
  }
});
