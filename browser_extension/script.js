async function fetchData(t_uri) {
    document.getElementById("returnedtxt").innerHTML = "";
    $('#returnedtxt').removeClass();
    $("#returned_news").removeClass();
    $("#loader").addClass("spinner-border text-primary");
    document.getElementById("returned_news").innerHTML = "";
    t_uri_array = t_uri.split("/");
    tweet_id = "";
    if (document.getElementById("tweet_id").value == "") {
        tweet_id = t_uri_array[5].substring(0, 19);
    } else {
        tweet_id = document.getElementById("tweet_id").value

    }
    alert(tweet_id);
    const res = await fetch("http://127.0.0.1:8080/inference", {
        method: "POST",
        body: JSON.stringify({ "tweet_id": tweet_id })
    });
    $("#loader").removeClass();
    const record = await res.json();
    document.getElementById("returnedtxt").innerHTML = record.classification;
    $('#returnedtxt').removeClass();
    $('#returnedtxt').addClass("col-auto");
    switch (record.classification) {
        case "Error":
            $('#returnedtxt').addClass("badge bg-danger");
            break;
        case "Non-rumour":
            $('#returnedtxt').addClass("badge bg-success");
            break;
        case "False":
            $('#returnedtxt').addClass("badge bg-danger");
            break;
        case "True":
            $('#returnedtxt').addClass("badge bg-success");
            break;
        case "Unverified":
            $('#returnedtxt').addClass("badge bg-warning");

    }
    $("#returned_news").addClass("card mx-auto border-primary card-header")
    document.getElementById("returned_news").style.width = "595px";
    $("#returned_news").append("<h2 class='card-title'>Related News Articles</h2>");
    let news = record.news;
    if (news.length == 0) {
        document.getElementById("returned_news").innerHTML = "We have not found any news articles associated to this Tweet.";
    } else {
        for (const article of news) {
            strUI = '<a href=' + article.url + ' target=_blank>' + article.title + '</a>';
            var time = new Date(article.publishedAt)
            var sourceName = "";
            if ("Name" in article.source) {
                sourceName = article.source.Name;
            } else {
                sourceName = article.source.name;
            }

            strCaption = '<font size=2><em>' + time.toLocaleString() + '</em><b> ' + sourceName + '</b></font>';
            $("#returned_news").append(strUI);
            $("#returned_news").append(strCaption + '<br/>');
        }

    }
}


document.getElementById('button').addEventListener('click', function (evt) {
    evt.preventDefault();
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
        let t_uri = tabs[0].url;
        fetchData(t_uri);
    });
})