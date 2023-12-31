function onOpen(){
  var ui = SpreadsheetApp.getUi() // mapeia toda a planilha onde os dados estão localizados
  ui.createMenu('Bruno Reina - PA 004')
  .addItem('Get Prediction', 'PredictAll') // toda vez que o usuário apertar o botão 'get prediction' irá rodar a função 'predict all'
  .addToUi()
}

// modelo em produção
host_production = 'https://health-insurance-api-omlh.onrender.com'

// chamada em API
function ApiCall(data, endpoint){
  var url = host_production + endpoint
  var payload = JSON.stringify(data); // transforma a string (dicionário) gerada na predição em um json

  var options = {'method': 'POST', 'contentType': 'application/json', 'payload': payload}

  Logger.log(url) // confere se a URL está correta
  Logger.log(options) // confere se as opções estão corretas

  var response = UrlFetchApp.fetch(url, options)

  // get response
  var rc = response.getResponseCode()
  var responseText = response.getContentText()

  if (rc !== 200){
    Logger.log('Response (%s) %s', rc, responseText)
  }
  else{
    prediction = JSON.parse(responseText)
  }
  return prediction
}

function PredictAll(){
  var ss = SpreadsheetApp.getActiveSheet()
  var lastColumn = ss.getLastColumn()
  var titleColumns = ss.getRange('A1' + ':' + lastColumn + '1').getValues()[0] // pega todas as colunas
  var lastRow = ss.getLastRow() // pega a última linha
    
  var data = ss.getRange('A2' + ':' + 'L' + lastRow).getValues() // indica que pega todos os valores da primeira até última célula
    
  // percorre todas as linhas da planilha
  for (row in data){
    var json = new Object()
        
    // percorre todas as colunas
    for (var j = 0; j < titleColumns.length; j++){
      json[titleColumns[j]] = data[row][j] // vai pegar cada coluna e atribuir o valor da linha correspondente
    }        
    
    // enviar o arquivo json
    var json_send = new Object()
    
    json_send['id'] = json['id']
    json_send['Gender'] = json['Gender']
    json_send['Age'] =  json['Age']
    json_send['Driving_License'] = json['Driving_License']
    json_send['Region_Code'] = json['Region_Code']
    json_send['Previously_Insured'] = json['Previously_Insured']
    json_send['Vehicle_Age'] = json['Vehicle_Age']
    json_send['Vehicle_Damage'] = json['Vehicle_Damage']
    json_send['Annual_Premium'] = json['Annual_Premium']
    json_send['Policy_Sales_Channel'] = json['Policy_Sales_Channel']
    json_send['Vintage'] = json['Vintage']

    // retorna a predição
    pred = ApiCall(json_send, '/healthinsurance/predict')
    
    // envia a predição para a coluna desejada (12) na planilha a partir da linha 2
    ss.getRange(Number(row)+2, lastColumn).setValue(pred[0]['score'])
    // vai começar a inserir os valores a partir da primeira linha na coluna chamada score
    Logger.log(pred[0])
    Logger.log(pred[0]['score'])
    Logger.log(row)
    
  }
}