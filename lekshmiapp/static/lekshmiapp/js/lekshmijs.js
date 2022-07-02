const btn=document.getElementById('id_employee_adharnos')
btn.addEventListener('change',myfunc)
function myfunc(event){
    alert('hello')
    const searchstring='ipo'
    fetch('iamfromfetch?' + new URLSearchParams({
    foo: 'value',
    bar: 2,
}))      
    .then(response=>{
    return response.json();
})
}
// const row=	this.closest("tr")
// const cell=row.cells[0].innerText
// const fname=document.getElementById('txtfname').value
// document.getElementById('txtlname').value=fname
// alert(fname)