
$credFile = 'D:\coding\traeCN_project\wqb\.env'
$cred = Get-Content $credFile -ErrorAction SilentlyContinue | Select-String 'WQ_AUTH'
if ($cred) {
  $tok = ($cred -split '=',2)[1].Trim()
  try {
    $h = @{ Authorization = ('Basic ' + $tok) }
    $r = Invoke-WebRequest -Uri 'https://api.worldquantbrain.com/alphas/e767nR9O/correlations/prod' -Headers $h -UseBasicParsing -TimeoutSec 60
    $r.Content
  } catch { 'ERR: ' + $_.Exception.Message }
} else { 'NOAUTH' }
