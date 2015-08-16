<?PhP
/*
 Keeping it simple, input city - query the db - output json
 This is a test to see who is faster, python or php!
*/

try{

    $stime = microtime(true);

    $dc = new mysqli("localhost", "user", "password", "database");

    $qcity = substr(stripslashes($_GET["city"]),0,100);

    $qcity = preg_replace('/\s+/', ' ', $qcity);
    $qcity = trim($qcity);

    if (strlen($qcity) < 3){
        throw new Exception('City should be at least 3 alphanumerics.');
    }

    $ssql = " select * from loc_cities where city like '".addslashes($qcity)."%' ";
    $rscities = $dc->query($ssql);
    while($row = $rscities->fetch_assoc()){
        $cities[] = array("city" => $row["city"],
                          "region" => $row["region"],
                          "lat" => $row["lat"],
                          "lon" => $row["lon"]);
    }

    $etime = microtime(true);
    $ttime = $etime - $stime;
    $mtime = $ttime * 1000;

    $html = "{";
    $html .= "\"qs\":\"".$qcity."\",";
    $html .= "\"ms\":\"".$mtime."\",";
    $html .= "\"cities\":".json_encode($cities);
    $html .= "}";

}catch(Exception $e){

    $html =  "{'error':'".$e->getMessage()."'}";

}finally{

    print $html;

}
?>
