<?php 
        
defined('BASEPATH') OR exit('No direct script access allowed');
        
class Testeftp extends CI_Controller {

    function __construct()
	{
		parent::__construct();
    }
public function imagem($primary_key)
{
    // dados do processo
    $this->load->model('home_model');
    $data = $this->home_model->seleciona($primary_key);

    // verificar $data->tipo e armazenar o diretório do ftp;
    if(in_array($data->tipo, array(2,5,6))) { // 2 a pagar; 5 indeferido
        ?> <script>
        alert("As Caixas/Pastas de \n\n>>>>> Processos A Pagar e de \n>>>>>>");
        history.back();
        </script> <?php
        return;            
    } elseif ($data->tipo == 3) { // canudos
        $this->canudos($data);
        return;
    } elseif ($data->tipo == 1) { // 1 pasta/caixa
        $pasta_ftp = '/Volume_1/Parcelamentos/Imagens Escaneadas/Pasta ';  
    } elseif ($data->tipo == 4) { // diversos
        $pasta_ftp = '/Volume_1/Parcelamentos/Processos_Diversos/DIVERSAS/Pasta';
    } elseif ($data->tipo == 7) { // averbações/fração ideal
        $pasta_ftp = '/Volume_1/Parcelamentos/Averbacoes-Fracao_Ideal/PROC_Pasta';
    }

    // $proc = $data[processo] alterando / por _
    $proc = str_replace('/', '_', $data->processo);
    // dividir pasta xxx/zz em $num_pasta = xxx e $seq = zz
    $pos = strpos($data->pasta, '/');
    $num_pasta = substr($data->pasta, 0, $pos);        
    $seq = substr($data->pasta, $pos + 1);

    // Dados do servidor FTP
    $servidor = '192.168.4.169'; // Endereço
    $usuario = 'luiz_fabris'; // Usuário
    $senha = 'f1nh44'; // Senha

    // Abre a conexão com o servidor FTP
    $ftpconn = ftp_connect($servidor, 21); // Retorno: true ou false
    // Verificar se a conexão foi bem-sucedida
    if (!$ftpconn) {
        // Conexão falhou
        $msg['msg'] = 'Falha na conexão com o Servidor FTP';
        $this->load->view('includes/html_erro', $msg);
        return;
    }

    // Faz o login no servidor FTP
    $login = ftp_login($ftpconn, $usuario, $senha); // Retorno: true ou false
    // Verificar se o login foi bem-sucedido
    if (!$login) {
        // Falha no login
        $msg['msg'] = 'Falha no login no Servidor FTP (Torradeira).';
        $this->load->view('includes/html_erro', $msg);
        return;
    } else {
        // Conexão e login bem-sucedidos
        // echo "conectado". "<br />";
    }
    
    ftp_pasv($ftpconn, true);
    // Recebe lista dos arquivos do ftp do 1º nível
    $pasta_ftp = $pasta_ftp . trim($num_pasta);
    $lista_pastas = ftp_nlist($ftpconn, $pasta_ftp);
    // echo 'pasta_ftp '.$pasta_ftp."<br/>";
    // echo 'lista pastas '.print_r($lista_pastas)."<br/>";
    if ($data->tipo == 4) {
        $proc = substr($proc, 0, strpos($proc, '_'));
    } 
    $proc_pesq = '['.$proc.']';

    $pesquisa = preg_grep($proc_pesq, $lista_pastas);
    // echo 'proc_pesq '.$proc_pesq."<br/>";
    // echo 'pesquisa '.print_r($pesquisa)."<br/>";
    if ($pesquisa == false) {
        $msg['msg'] = 'Processo não localizado. Verifique com o Arquivo Par';
        $this->load->view('includes/html_erro', $msg);
        return;
    } else {
        $local_ftp = $pasta_ftp . '/' . implode('', $pesquisa);
        $arquivos = ftp_nlist($ftpconn, $local_ftp);
        $data_array = get_object_vars($data);
        $i = 0;
        foreach ($arquivos as $arquivo) {
            if ($i > 1 and $arquivo <> 'Thumbs.db') {
                $old_file = $local_ftp . '/' . $arquivo;
                $excluir = array('[', '{', '(', ')', ',', ';', '|', '!', '"', '@', '#');
                $str = str_replace($excluir, '', $arquivo);   // elimina caracteres especiais
                $new_file = $local_ftp . '/' . str_replace(" ", "_", preg_replace("/&(.*?);/i", "", $str));
                ftp_rename($ftpconn, $old_file, $new_file);
                $data->arquivos[$i] = str_replace(" ", "_", preg_replace("/&(.*?);/i", "", $arquivo));
            }
            $i++;
        }
        // Fecha conexão ftp
        ftp_close($ftpconn);
        $_SESSION['dps']['local_ftp'] = $local_ftp;
        //unset($data->arquivos[0]); // notação de diretório .
        //unset($data->arquivos[1]); // notação de diretório ..
        $this->load->view('ftp_view1', $data);
    }
}

    public function imagem_bkp($primary_key)
    {
        // dados do processo
        $this->load->model('home_model');
		$data = $this->home_model->seleciona($primary_key);
  
        // verificar $data->tipo e armazenar o diretório do ftp;
        if(in_array($data->tipo, array(2,5,6))) {       // 2 a pagar; 5 indeferidos; 6 suspensas. NÃO ESCANEADAS!
            ?> <script>
            alert("As Caixas/Pastas de \n\n>>>>> Processos A Pagar e de \n>>>>> Processos Indeferidos e as \n>>>>> Pastas Suspensas \n\nnão foram escaneados!!!");
            history.back();
            </script> <?php
            return;            
        } elseif ($data->tipo == 3) {   // canudos
            $this->canudos($data);                     
            return;
        } elseif ($data->tipo == 1) {         // 1 pasta/caixa
            $pasta_ftp = '/Volume_1/Parcelamentos/Imagens Escaneadas/Pasta ';    
        } elseif ($data->tipo == 4) {   // diversos
            $pasta_ftp = '/Volume_1/Parcelamentos/Processos_Diversos/DIVERSAS/Pasta ';  
        } elseif ($data->tipo == 7) {   // averbações/fração ideal
            $pasta_ftp = '/Volume_1/Parcelamentos/Averbacoes-Fracao_Ideal/PROC_AVERBACAO/Caixa ';  
        }

        // $proc = $data[processo] alterando / por _
        $proc = str_replace('/','_',$data->processo);
        // dividir pasta xxx/zz em $num_pasta = xxx e $seq = zz
        $pos = strpos($data->pasta,'/');
        $num_pasta = substr($data->pasta,0,$pos);        
        $seq = substr($data->pasta,$pos+1);

        // Dados do servidor FTP
        $servidor = '192.168.4.169'; // Endereço
        $usuario = 'luiz_fabris'; // Usuário
        $senha = 'f1nh44'; // Senha
        // Abre a conexão com o servidor FTP
        $ftpconn = ftp_connect($servidor); // Retorno: true ou false
        // Faz o login no servidor FTP
        $login = ftp_login($ftpconn, $usuario, $senha); // Retorno: true ou false
        // Informa sucesso ou não da conexão
        if (isset($login) and $login == true) {
            //echo "conectado". "<br />";
        }else{
            //echo "Falha na conexão com o Servidor FTP (Torradeira).";
            $msg['msg'] = 'Falha na conexão com o Servidor FTP (Torradeira). Fale com o Administrador!';
            $this->load->view('includes/html_erro',$msg);
            return;
        }

         // Recebe lista dos arquivos do ftp do 1º nível
        $pasta_ftp = $pasta_ftp . trim($num_pasta);
        $lista_pastas = ftp_nlist($ftpconn,$pasta_ftp);
        //echo 'pasta_ftp '.$pasta_ftp.br();
        //echo 'lista pastas '.print_r($lista_pastas).br();
        if ($data->tipo == 4) {
            $proc = substr($proc,0,strpos($proc,'_'));
        } /*elseif($data->tipo == 3) {
            $proc = $data->pasta;
        }*/
        $proc_pesq = '['.$proc.']';
  
        $pesquisa = preg_grep($proc_pesq, $lista_pastas);
        //echo 'proc_pesq '.$proc_pesq.br();
        //echo 'pesquisa '.print_r($pesquisa).br();
        if ($pesquisa == false) {
            $msg['msg'] = 'Processo não localizado. Verifique com o Arquivo Parcelamentos.';
            $this->load->view('includes/html_erro',$msg);
            return;
        }else{
            $local_ftp = $pasta_ftp.'/'.implode('', $pesquisa);
            $arquivos = ftp_nlist($ftpconn, $local_ftp);
            $data_array = get_object_vars($data);
            $i = 0;
            foreach($arquivos as $arquivo) {
                if ($i > 1 and $arquivo <> 'Thumbs.db') {
                    $old_file = $local_ftp.'/'.$arquivo;
                    $excluir = array('[','{','(',')',',',';','|','!','"','@','#','$','%','&','~','^','ª','º','}',']');
                    $str = str_replace($excluir, '', $arquivo);   // elimina esses caracteres especiais!
                    $new_file = $local_ftp.'/'.str_replace(" ","_",preg_replace("/&([a-z])[a-z]+;/i", "$1", htmlentities(trim($str))));
                    ftp_rename($ftpconn, $old_file, $new_file);
                    $data->arquivos[$i] = str_replace(" ","_",preg_replace("/&([a-z])[a-z]+;/i", "$1", htmlentities(trim($str))));
                }
                $i++;                
            }
            // Fecha conexão ftp
            ftp_close($ftpconn);
            $_SESSION['dps']['local_ftp'] = $local_ftp;
            //unset($data->arquivos[0]);      // notação de diretório .
            //unset($data->arquivos[1]);      // notação de diretório ..
            $this->load->view('ftp_view1', $data);
        }
    }

 function canudos($data)
    {
        $local_ftp = '/Volume_1/Parcelamentos/Canudos/Canudo ' . $data->pasta; 
        $servidor = '192.168.4.169';
        $usuario = 'luiz_fabris';
        $senha = 'f1nh44';
    
        // Verifica conexão FTP
        $ftpconn = ftp_connect($servidor);
        if (!$ftpconn) {
            die("Erro: Não foi possível conectar ao servidor FTP.");
        }
    
        $login = ftp_login($ftpconn, $usuario, $senha);
        if (!$login) {
            die("Erro: Login no servidor FTP falhou.");
        }
    
        $arquivos = ftp_nlist($ftpconn, $local_ftp);
        if ($arquivos === false) {
            die("Erro: Não foi possível listar os arquivos do diretório FTP.");
        }
    
        // Verifica se $data->arquivos está inicializado
        if (!isset($data->arquivos)) {
            $data->arquivos = [];
        }
    
        $i = 0;
        foreach ($arquivos as $arquivo) {
            if ($i > 1 && $arquivo !== 'Thumbs.db') {
                $old_file = $local_ftp . '/' . $arquivo;
                $excluir = array('[','{','(',')',',',';','|','!','"','@','#','$','%','&','~','^','ª','º','}',']');
                $str = str_replace($excluir, '', $arquivo);
                $new_file = $local_ftp . '/' . str_replace(" ", "_", preg_replace("/&([a-z])[a-z]+;/i", "$1", htmlentities(trim($str), ENT_QUOTES, 'UTF-8')));
    
                // Renomeia arquivo no FTP
                if (!ftp_rename($ftpconn, $old_file, $new_file)) {
                    echo "Erro ao renomear o arquivo: $old_file\n";
                } else {
                    $data->arquivos[$i] = str_replace(" ", "_", preg_replace("/&([a-z])[a-z]+;/i", "$1", htmlentities(trim($str), ENT_QUOTES, 'UTF-8')));
                }
            }
            $i++;
        }
    
        // Fecha conexão FTP
        ftp_close($ftpconn);
    
        $_SESSION['dps']['local_ftp'] = $local_ftp;
    
        // Carrega a view com os dados
        $this->load->view('ftp_view1', $data);
    }
    function canudos_bkp($data)
    {
        $local_ftp = '/Volume_1/Parcelamentos/Canudos/Canudos/Canudo '.$data->pasta; 
        $servidor = '192.168.4.169'; // Endereço
        $usuario = 'luiz_fabris'; // Usuário
        $senha = 'f1nh44'; // Senha
        // Abre a conexão com o servidor FTP
        $ftpconn = ftp_connect($servidor); // Retorno: true ou false
        // Faz o login no servidor FTP
        $login = ftp_login($ftpconn, $usuario, $senha); // Retorno: true ou false
        $arquivos = ftp_nlist($ftpconn, $local_ftp);
        $data_array = get_object_vars($data);

        $i = 0;
        foreach($arquivos as $arquivo) {
            if ($i > 1 and $arquivo <> 'Thumbs.db') {
                $old_file = $local_ftp.'/'.$arquivo;
                $excluir = array('[','{','(',')',',',';','|','!','"','@','#','$','%','&','~','^','ª','º','}',']');
                $str = str_replace($excluir, '', $arquivo);   // elimina esses caracteres especiais!
                $new_file = $local_ftp.'/'.str_replace(" ","_",preg_replace("/&([a-z])[a-z]+;/i", "$1", htmlentities(trim($str))));
                ftp_rename($ftpconn, $old_file, $new_file);
                $data->arquivos[$i] = str_replace(" ","_",preg_replace("/&([a-z])[a-z]+;/i", "$1", htmlentities(trim($str))));
            }
        $i++;                
        }
        // Fecha conexão ftp
        ftp_close($ftpconn);
        $_SESSION['dps']['local_ftp'] = $local_ftp;
        //unset($data->arquivos[0]);      // notação de diretório .
        //unset($data->arquivos[1]);      // notação de diretório ..
        $this->load->view('ftp_view1', $data);
        return;
    }

    function abre($arquivo)
	{
		$SERVER_ADDRESS="192.168.4.169";
		$SERVER_USERNAME="luiz_fabris";
		$SERVER_PASSWORD="f1nh44";
		$conn_id = ftp_connect($SERVER_ADDRESS);
		// login with username and password
		$login_result = ftp_login($conn_id, $SERVER_USERNAME, $SERVER_PASSWORD);
		
		$server_file=$_SESSION['dps']['local_ftp'].'/'. $arquivo;
		$local_file = basename($server_file);
        
		// DOWNLOAD $SERVER_FILE AND SAVE TO $LOCAL_FILE
		if (ftp_get($conn_id, $local_file, $server_file, FTP_BINARY)) {
			$type = filetype($local_file);
			$size = filesize($local_file);
			header("Content-Description: File Transfer");
			header("Content-Type:{$type}");
			header("Content-Length:{$size}");
			header("Content-Disposition: attachment; filename=\"" . $local_file . "\"");
			//Faz download
			readfile($local_file);
			//Apaga o arquivo temporário
			unlink($local_file);
		} else {
			echo "OPS. Temos um problema.\n\n Fale com o Administrador.";
            ftp_close($conn_id);
            echo br(3);
            echo anchor ('home/busca/', ' RETORNAR ', array('class' => 'btn btn-default btn-warning'));

		}
		ftp_close($conn_id);
	}

}
        
    /* End of file  testeftp.php */
        
                            
