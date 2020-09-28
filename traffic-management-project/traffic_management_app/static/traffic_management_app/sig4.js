function redLight(stop,left,go,right){
	clearall(stop,left,go,right);
	document.getElementById(stop).style.backgroundColor="red";
	}

function greenLight(stop,left,go,right){
	clearall(stop,left,go,right);
	document.getElementById(go).style.backgroundColor="green";
}

function leftLight(stop,left,go,right){
	clearall(stop,left,go,right);
	document.getElementById(left).style.backgroundColor="green";
}

function rightLight(stop,left,go,right){
	clearall(stop,left,go,right);
	document.getElementById(right).style.backgroundColor="green";
}
function clearall(stop,left,go,right){
	document.getElementById(stop).style.backgroundColor="black";
	document.getElementById(go).style.backgroundColor="black";
	document.getElementById(left).style.backgroundColor="black";
	document.getElementById(right).style.backgroundColor="black";
}

function call_sig1(stop,left,go,right){
	document.getElementById(stop)=redLight(stop,left,go,right);	
	document.getElementById(go)=greenLight(stop,left,go,right);
	document.getElementById(left)=leftLight(stop,left,go,right);
	document.getElementById(right)=rightLight(stop,left,go,right);
}

function call_sig2(stop,left,go,right){
	document.getElementById(stop)=redLight(stop,left,go,right);	
	document.getElementById(go)=greenLight(stop,left,go,right);
	document.getElementById(left)=leftLight(stop,left,go,right);
	document.getElementById(right)=rightLight(stop,left,go,right);
}

function call_sig3(stop,left,go,right){
	document.getElementById(stop)=redLight(stop,left,go,right);	
	document.getElementById(go)=greenLight(stop,left,go,right);
	document.getElementById(left)=leftLight(stop,left,go,right);
	document.getElementById(right)=rightLight(stop,left,go,right);
}

function call_sig4(stop,left,go,right){
	document.getElementById(stop)=redLight(stop,left,go,right);	
	document.getElementById(go)=greenLight(stop,left,go,right);
	document.getElementById(left)=leftLight(stop,left,go,right);
	document.getElementById(right)=rightLight(stop,left,go,right);
}
