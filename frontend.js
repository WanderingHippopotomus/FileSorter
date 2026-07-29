const startSort = async () => {
    if (status === "sorting") return;

    setStatus("sorting");

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/sort",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    directory: path
                })
            }
        );

        const data = await response.json();

        setProgress(100);

        setResult(data);

        setStatus("done");

    } catch (err) {

        console.error(err);

        alert("Sorting failed.");

        setStatus("idle");

    }
};