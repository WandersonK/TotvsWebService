-- Informar seu schema abaixo
CREATE TABLE <schema>.rm_ppessoa (
	codigo int4 NOT NULL,
	nome varchar(120) NULL,
	apelido varchar(40) NULL,
	dtnascimento date NULL,
	estadocivil varchar(1) NULL,
	rua varchar(140) NULL,
	sexo varchar(1) NULL,
	numero varchar(8) NULL,
	nacionalidade varchar(3) NULL,
	complemento varchar(60) NULL,
	grauinstrucao varchar(3) NULL,
	bairro varchar(80) NULL,
	estado varchar(2) NULL,
	cidade varchar(32) NULL,
	cep varchar(9) NULL,
	pais varchar(20) NULL,
	idimagem int4 NULL,
	regprofissional varchar(15) NULL,
	cpf varchar(11) NULL,
	telefone1 varchar(20) NULL,
	telefone2 varchar(20) NULL,
	cartidentidade varchar(15) NULL,
	ufcartident varchar(2) NULL,
	email varchar(60) NULL,
	orgemissorident varchar(20) NULL,
	fax varchar(15) NULL,
	dtemissaoident date NULL,
	reccreatedby varchar(20) NULL,
	tituloeleitor varchar(20) NULL,
	reccreatedon timestamp without time zone NULL,
	zonatiteleitor varchar(20) NULL,
	recmodifiedby varchar(20) NULL,
	secaotiteleitor varchar(6) NULL,
	recmodifiedon timestamp without time zone NULL,
	carteiratrab varchar(10) NULL,
	codcoligada int4 NULL,
	seriecarttrab varchar(5) NULL,
	ufcarttrab varchar(2) NULL,
	dtcarttrab date NULL,
	nit smallint NULL,
	cartmotorista varchar(15) NULL,
	tipocarthabilit varchar(10) NULL,
	dtvenchabilit date NULL,
	certifreserv varchar(40) NULL,
	categmilitar varchar(10) NULL,
	naturalidade varchar(32) NULL,
	estadonatal varchar(2) NULL,
	datachegada date NULL,
	cartmodelo19 varchar(15) NULL,
	conjugebrasil smallint NULL,
	naturalizado smallint NULL,
	filhosbrasil smallint NULL,
	nrofilhosbrasil smallint NULL,
	nroreggeral varchar(20) NULL,
	nrodecreto varchar(20) NULL,
	dtvencident date NULL,
	dtvenccarttrab date NULL,
	tipovisto varchar(20) NULL,
	investtreinant numeric NULL,
	corraca smallint NULL,
	deficientefisico smallint NULL,
	codusuario varchar(20) NULL,
	telefone3 varchar(20) NULL,
	empresa varchar(60) NULL,
	codprofissao int4 NULL,
	codocupacao varchar(3) NULL,
	codmemoobs int4 NULL,
	brpdh smallint NULL,
	npassaporte varchar(15) NULL,
	fumante smallint NULL,
	paisorigem varchar(50) NULL,
	dtemisspassaporte date NULL,
	dtvalpassaporte date NULL,
	obspessoa varchar(50) NULL,
	idimagemdoc int4 NULL,
	idimagemdocv int4 NULL,
	ajustatamanhofoto smallint NULL,
	deficienteauditivo smallint NULL,
	deficientefala smallint NULL,
	deficientevisual smallint NULL,
	deficientemental smallint NULL,
	recursorealizacaotrab varchar(120) NULL,
	recursoacessibilidade varchar(120) NULL,
	dataaprovacaocurr date NULL,
	codmunicipio varchar(20) NULL,
	localidade varchar(40) NULL,
	csm varchar(10) NULL,
	dtexpcml date NULL,
	exped varchar(10) NULL,
	rm varchar(10) NULL,
	sitmilitar varchar(10) NULL,
	dttiteleitor date NULL,
	esteleit varchar(2) NULL,
	tiposang varchar(10) NULL,
	idbiometria int4 NULL,
	aluno smallint NULL,
	professor smallint NULL,
	usuariobiblios smallint NULL,
	funcionario smallint NULL,
	exfuncionario smallint NULL,
	candidato smallint NULL,
	tagscript varchar(1) NULL,
	fiador_sgi smallint NULL,
	conjuge_sgi smallint NULL,
	deficientemobreduzida smallint NULL,
	dtvencidentpt date NULL,
	codtiporua smallint NULL,
	codtipobairro smallint NULL,
	codnaturalidade varchar(20) NULL,
	numeroric varchar(20) NULL,
	orgemissorric varchar(20) NULL,
	dtemissaoric date NULL,
	dtemissaocnh date NULL,
	orgemissorcnh varchar(20) NULL,
	datanaturalizacao date NULL,
	orgemissorrne varchar(20) NULL,
	dtemissaorne date NULL,
	nomesocial varchar(120) NULL,
	idpais smallint NULL,
	deficienteintelectual smallint NULL,
	deficienteobservacao varchar(255) NULL,
	dataobito date NULL,
	matriculaobito varchar(50) NULL,
	falecido int4 NULL,
	portarianaturalizacao varchar(50) NULL,
	codclassiftrabestrang varchar(20) NULL,
	ufcnh varchar(2) NULL,
	dataprimeiracnh date NULL,
	ano1emprego int4 NULL,
	emailpessoal varchar(60) NULL,
	tipoprazoresidencia smallint NULL
);

-- Informar seu schema abaixo
CREATE UNIQUE INDEX idx_ppessoa_idx ON <schema>.rm_ppessoa USING btree (codigo);
CREATE INDEX idx_rm_ppessoa_codigo ON <schema>.rm_ppessoa USING btree (codigo);
CREATE INDEX idx_rm_ppessoa_nome ON <schema>.rm_ppessoa USING btree (nome);
