document.getElementById("rss-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const rssFeed = document.getElementById("rss-feed").value;
    console.log(`输入的 RSS 订阅源: ${rssFeed}`);
    const response = await fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `rss_feed=${encodeURIComponent(rssFeed)}`
    });

    if (response.ok) {
        const data = await response.json();
        console.log(`返回的新 RSS 订阅源: ${data.new_feed}`);
        document.getElementById("result").value = data.new_feed;
    } else {
        alert("生成新的 RSS 订阅源时出错，请稍后重试。");
    }
});