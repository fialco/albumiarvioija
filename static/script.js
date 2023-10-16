var trackform = document.getElementById("trackform");

function add(){
  var newField = document.createElement("input");
  newField.setAttribute("type","text");
  newField.setAttribute("name","track_name");
  newField.setAttribute("size",50);
  newField.setAttribute("placeholder","Kappaleen nimi");
  newField.setAttribute("required","");
  trackform.appendChild(newField);

  var newField = document.createElement("input");
  newField.setAttribute("type","float");
  newField.setAttribute("name","track_length");
  newField.setAttribute("size",10);
  newField.setAttribute("placeholder","Pituus");
  newField.setAttribute("required","");
  trackform.appendChild(newField);
}

function remove(){
  var input_tags = trackform.getElementsByTagName("input");
  if(input_tags.length > 2) {
    trackform.removeChild(input_tags[(input_tags.length) - 1]);
    trackform.removeChild(input_tags[(input_tags.length) - 1]);
  }
}