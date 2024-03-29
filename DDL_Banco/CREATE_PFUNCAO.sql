-- Informar seu schema abaixo
CREATE TABLE <schema>.rm_pfuncao (
    CODCOLIGADA smallint NOT NULL,
    CODIGO VARCHAR(10) NOT NULL,
    NOME VARCHAR(100) NULL,
    NUMPONTOS smallint NULL,
    CBO VARCHAR(8) NULL,
    DESCRICAO TEXT NULL,
    CARGO VARCHAR(16) NULL,
    INATIVA smallint NULL,
    ATIVTRANSP smallint NULL,
    FAIXASALARIAL VARCHAR(16) NULL,
    LIMITEFUNC int4 NULL,
    VERBAQUADROVAGAS smallint NULL,
    PERCQUADROVAGAS smallint NULL,
    DATAULTIMAREVISAO date NULL,
    NUMREVISAO VARCHAR(30) NULL,
    CBO2002 VARCHAR(10) NULL,
    CODTABELA VARCHAR(10) NULL,
    CODPERFILCAND VARCHAR(15) NULL,
    ID int4 NOT NULL,
    BENEFPONTOS int4 NULL,
    OBJETIVO varchar(255) NULL,
    DESCRICAOPPP TEXT NULL,
    EXIBEORGANOGRAMA VARCHAR(1) NULL,
    CODFUNCAOCHEFIA VARCHAR(10) NULL,
    JORNADAREF smallint NULL,
    RECCREATEDBY VARCHAR(50) NULL,
    RECCREATEDON timestamp without time zone NULL,
    RECMODIFIEDBY VARCHAR(50) NULL,
    RECMODIFIEDON timestamp without time zone NULL,
    CODTIPOFUNCAO CHAR(2) NULL,
    SIGLA VARCHAR(30) NULL,
    CODCLASSFUNCAO VARCHAR(3) NULL,
    ESOCIALFUNCAOCONF smallint NULL,
    SIMILARIDADEINTEGRACAOGUPY int4 NULL 
);

-- Informar seu schema abaixo
CREATE INDEX idx_pfuncao_idx ON <schema>.rm_pfuncao USING btree (codcoligada, codigo);
