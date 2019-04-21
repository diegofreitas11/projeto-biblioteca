

function escolher_livro(inicio, valido, texto, nome){
    var node;
    var text;
    if (inicio == 0){
        if (valido == 0){
            document.getElementById("procurar_aluno").style.borderColor = "red";
            document.getElementById("label_invalido").style.display = "block";
        }else{
            node = document.createElement("SPAN");
            text = document.createTextNode(nome);
            node.appendChild(text);
            document.getElementById("pesquisa_aluno").appendChild(node);
            document.getElementById("escolher-livro").style.display = "block";
            document.getElementById("procurar_aluno").style.border = "1px solid black";
            document.getElementById("procurar_aluno").value = texto;
            document.getElementById("procurar_aluno").readOnly = true;
            document.getElementById("label_invalido").style.display = "none";
        }
    }
}

function preencher_campos(campos, tipo){
    if(tipo=="aluno"){
        document.getElementById("txt_matricula").value = campos[0];
        document.getElementById("txt_matricula").readOnly = true;
        document.getElementById("txt_nome").value = campos[1];
        document.getElementById("txt_rg").value = campos[2];
        document.getElementById("txt_periodo").value = campos[3];
        document.getElementById("txt_ano").value = campos[4];
        document.getElementById("txt_senha").value = campos[5];
    }else{
        document.getElementById("txt_descr").value = campos[0];
        document.getElementById("txt_nome").value = campos[1];
        document.getElementById("txt_genero").value = campos[2];
        document.getElementById("txt_autor").value = campos[3];
        document.getElementById("txt_ano").value = campos[4];
        document.getElementById("txt_qtd").value = campos[5];
        document.getElementById("txt_editora").value = campos[6];
        document.getElementById("txt_id").value = campos[7];
    }

    if(campos[1]!=" "){
        var btn = document.getElementById("btn_cadastrar");
        btn.innerHTML = "Editar";
        btn.value = "upgrade";
    }

}

