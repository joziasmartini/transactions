let conn;
let i = 0;
var tmp; 

//var timerId = setTimeout(function() { alert(1) }, 5000);
async function runTransaction_imp(){
  await execute_implicit(); // comando com tempos implicitos de inserção   
  await showRows();
}

async function runTransaction() {
    //Get form values
    //let numTuples = document.getElementById("tuples").value;
    //let timeToInsert = getTimeToInsert();
      
    //Print in interface to test
    //let test = document.getElementById("test");
    //test.innerHTML = `
    //Number of tuples inserted: ${numTuples}<br>
    //Time to insert the tuples: ${timeToInsert} ms<br>
    //`;

    //Connect and insert
    connect();
    await createTable();
    await execute(); // comando com insert explícito
  //await execute_implicit(); // comando com tempos implicitos de inserção   
    await showRows();
}

//Generate random string to client name
function getRandomString() {
    let result = '';
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    let charactersLength = characters.length;
    let length = 9;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

//Generate random number to client id, cpf, saldoemconta
function getRandomNumber() {
  let result = '';
  let length = 9;
  for ( var i = 0; i < length; i++ ) {
    result += Math.floor(Math.random() * 10);
  }
  return result;
}

//Connect to database with postgres user and pass
function connect() {
    const { Client } = require('pg');
    conn = new Client({
        host: 'localhost',
        database: 'transaction_db',
        user: 'postgres',
        password: '1234',
        port: 5432,
  });
  conn.connect();
}

//Create table after connect
async function createTable() {
    await conn.query(`
        drop table if exists clientes;
        create table if not exists clientes(
            id integer not null,
            nome varchar,
            cpf integer, 
            dataNascimento date,
            saldoEmConta integer,
            primary key (id)
        )
    `);
  console.log('Table created in postgresql');
}

//Execute implicit
async function execute_implicit(){
  today = new Date();
  while (i < 20000) {
    try {
        const sqlString = `INSERT INTO clientes (id, nome, cpf, datanascimento, saldoemconta) VALUES ($1, $2, $3, $4, $5);`;
        const values = [getRandomNumber(), getRandomString(), getRandomNumber(), '2020-11-11', getRandomNumber()];

        //Pass sql string to the query method
        await conn.query(sqlString, values, function(err, result) {
        console.log("client.query() SQL result:", result);
        if (err) {
            console.log("\nclient.query():", err);
        } 
      });
    } catch (er) {
      // Rollback before executing another transaction
      console.log("client.query():", er);
    }
    i++
  }

} 

//Execute explicit
async function execute(){
  //await conn.query('SET AUTOCOMMIT = 0');  
  try {
    today = new Date();
      //Init the postgres transaction
      await conn.query("BEGIN");
      //Insert 100k tuples
      while (i < 20000) {
          let id = getRandomNumber();
          let nome = getRandomString();
          let cpf = getRandomNumber();
          let datanascimento = "2020-11-11"
          let saldoemconta = getRandomNumber();
  
          try {
              //Declare string for sql statement
              const sqlString = `INSERT INTO clientes (id, nome, cpf, datanascimento, saldoemconta) VALUES ($1, $2, $3, $4, $5);`;
              const values = [id, nome, cpf, datanascimento, saldoemconta];
      
              //Pass sql string to the query method
              await conn.query(sqlString, values, function(err, result) {
              console.log("client.query() SQL result:", result);
      
              if (err) {
                  console.log("\nclient.query():", err);
        
                  //Rollback before executing another transaction
                  conn.query("ROLLBACK");
                  console.log("Transaction ROLLBACK called");
              } else {
                  conn.query("COMMIT");
                  console.log("client.query() COMMIT row count:", result.rowCount);
              }
          });
          } catch (er) {
            //Rollback before executing another transaction
            conn.query("ROLLBACK");
            console.log("client.query():", er);
            console.log("Transaction ROLLBACK called");
          }
          i++
      }
  } finally {
      console.log("Client is released");
    }
}

//Print all rows in console
async function showRows() {

  let { rows } = await conn.query(`select * from clientes`);
  for (const row of rows) {
    console.log(row);
  }
  tmp = (new Date() - today);
  console.log("\nWas inserted " + i + " rows in" + tmp + " ms(t)");

  //Kill process in node, go back terminal
  process.exit();
}

runTransaction();
//runTransaction_imp();