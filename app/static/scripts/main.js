const statusLight = document.querySelector(".status-light");
const discoveryProgress = document.querySelector(".discovery-progress");
const discoverBtn = document.getElementById("discover-btn");
const muteBtn = document.querySelector(".mute-btn");

function sendCommand(command) {
	fetch("/control", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ command: command }),
	})
		.then((response) => response.json())
		.then((data) => {
			if (data.success) {
				console.log("Command sent successfully");
				if (command === "mute") {
					muteBtn.textContent = data.mute_status ? "Unmute" : "Mute";
				}
			} else {
				console.error(data.message);
			}
		})
		.catch((error) => {
			console.error(error);
		});
}

document.querySelectorAll(".btn").forEach((button) => {
	button.addEventListener("click", function () {
		const command = this.textContent.toLowerCase().replace(/\s/g, "");
		if (command == "discover") return;
		console.log(command.trim());
		sendCommand(command);
	});
});

function changeConnectivityStatus(state) {
	if (state === "connected") {
		statusLight.style.backgroundColor = "green";
		discoverBtn.textContent = "Connected";
		discoverBtn.disabled = true;
		discoverBtn.classList.remove("btn-primary");
		discoverBtn.classList.add("btn-success");
	} else if (state === "disconnected") {
		statusLight.style.backgroundColor = "red";
		discoverBtn.textContent = "Discover";
		discoverBtn.disabled = false;
		discoverBtn.classList.remove("btn-success");
		discoverBtn.classList.add("btn-primary");
	} else if (state === "discovering") {
		statusLight.style.backgroundColor = "yellow";
		discoverBtn.textContent = "Discovering...";
		discoverBtn.disabled = true;
		discoverBtn.classList.remove("btn-primary");
		discoverBtn.classList.add("btn-warning");
	}
}

discoverBtn.addEventListener("click", function () {
	changeConnectivityStatus("discovering");
	fetch("/discover", { method: "POST" })
		.then((response) => response.text())
		.then((responseText) => {
			const jsonObjects = responseText.trim().split(/}\s*{/);
			jsonObjects.forEach((jsonObject, index) => {
				try {
					const data = JSON.parse(
						(index > 0 ? "{" : "") +
							jsonObject +
							(index < jsonObjects.length - 1 ? "}" : "")
					);
					if (data.success) {
						discoveryProgress.textContent = data.message;
						if (data.message === "Discovery completed.") {
							changeConnectivityStatus("connected");
							localStorage.setItem("tvConnectionStatus", "connected");
						}
					} else {
						changeConnectivityStatus("disconnected");
						console.error(data.message);
					}
				} catch (error) {
					console.error("Error parsing JSON object:", error);
					console.error("JSON object:", jsonObject);
					changeConnectivityStatus("disconnected");
				}
			});
		})
		.catch((error) => {
			console.error("Error connecting to TV:", error);
			changeConnectivityStatus("disconnected");
		});
});

document.getElementById("power-btn").addEventListener("click", function () {
	sendCommand("power");
});

// // Check connection status on page load
// window.addEventListener("DOMContentLoaded", function () {
// 	const tvConnectionStatus = localStorage.getItem("tvConnectionStatus");
// 	if (tvConnectionStatus === "connected") {
// 		changeConnectivityStatus("connected");
// 	} else {
// 		changeConnectivityStatus("disconnected");
// 	}
// });

window.addEventListener("DOMContentLoaded", function () {
	checkConnectionStatus();
});

function checkConnectionStatus() {
	fetch("/status", { method: "GET" })
		.then((response) => response.json())
		.then((data) => {
			if (data.connected) {
				changeConnectivityStatus("connected");
				localStorage.setItem("tvConnectionStatus", "connected");
			} else {
				changeConnectivityStatus("disconnected");
				localStorage.removeItem("tvConnectionStatus");
			}
		})
		.catch((error) => {
			console.error("Error checking connection status:", error);
			changeConnectivityStatus("disconnected");
			localStorage.removeItem("tvConnectionStatus");
		});
}
