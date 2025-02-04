document.addEventListener("DOMContentLoaded", () => {
    // モーダルの処理
    setupModals();

    // グラフの描画
    Chart.register(ChartDataLabels);
    renderPieChart("incomeData", "incomeChartContainer", "incomePieChart");
    renderPieChart("expenseData", "expenseChartContainer", "expensePieChart");
});

// ========================
// モーダルのセットアップ関数
// ========================
function setupModals() {
    const editModal = document.getElementById("editModal");
    if (editModal) {
        editModal.addEventListener("show.bs.modal", (event) => {
            const button = event.relatedTarget;
            editModal.querySelector("#modalId").value = button.getAttribute("data-id");
            editModal.querySelector("#modalName").value = button.getAttribute("data-name");
            editModal.querySelector("#modalAmount").value = button.getAttribute("data-amount");
            editModal.querySelector("#modalDate").value = button.getAttribute("data-date");
            editModal.querySelector("#modalTransaction_type").value = button.getAttribute("data-transaction_type");

            // カテゴリの選択を更新
            const modalCategoryInput = editModal.querySelector("#modalCategory");
            const category = button.getAttribute("data-category");
            modalCategoryInput.querySelectorAll("option").forEach(option => {
                option.selected = option.value === category;
            });
        });
    }

    const deleteModal = document.getElementById("deleteModal");
    if (deleteModal) {
        deleteModal.addEventListener("show.bs.modal", (event) => {
            const button = event.relatedTarget;
            deleteModal.querySelector("#modalId").value = button.getAttribute("data-id");
        });
    }
}

// ========================
// グラフを描画する関数
// ========================
function renderPieChart(dataElementId, containerId, canvasId) {
    const dataElement = document.getElementById(dataElementId);
    if (!dataElement) return;
    

    const data = JSON.parse(dataElement.textContent);
    const labels = data.labels;
    const values = data.values;
    const container = document.getElementById(containerId);
    const canvas = document.getElementById(canvasId);

    if (labels.length === 0 || values.length === 0) {
        // データがない場合の処理
        canvas.style.display = "none";
        const message = document.createElement("p");
        message.textContent = "データがありません";
        message.style.textAlign = "center";
        message.style.fontSize = "18px";
        message.style.color = "gray";
        container.appendChild(message);
    } else {
        // グラフを描画
        new Chart(canvas.getContext("2d"), {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { position: "bottom" },
                    datalabels: {
                        formatter: (value, context) => {
                            let total = context.dataset.data.reduce((sum, v) => sum + v, 0);
                            return ((value / total) * 100).toFixed(2) + "%";
                        },
                        color: "white",
                        font: { size: 14, weight: "bold" },
                        anchor: "center",
                        align: "center"
                    }
                }
            }
        });
    }
}


