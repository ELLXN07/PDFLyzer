async function analyzePDF(){

const file=
document
.getElementById(
"pdf"
)
.files[0]

if(!file){

alert(
"Select PDF first"
)

return

}

document
.getElementById(
"loading"
)
innerText=
"Analyzing..."

const form=
new FormData()

form.append(
"file",
file
)

try{

const response=

await fetch(

"/analyze-pdf",

{
method:"POST",

body:form
}

)

const data=

await response.json()

document
.getElementById(
"output"
)
.innerText=

data.analysis

}
catch{

document
.getElementById(
"output"
)
.innerText=

"Error"

}

document
.getElementById(
"loading"
)
.innerText=""

}