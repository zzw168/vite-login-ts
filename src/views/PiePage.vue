<template>
  <div>
    <h2>{{ title }}</h2>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { Chart, PieController, ArcElement, Tooltip, Legend } from "chart.js";

// 注册组件
Chart.register(PieController, ArcElement, Tooltip, Legend);

export default defineComponent({
  name: "PieChart",
  props: {
    title: {
      type: String,
      default: "饼状图示例",
    },
  },
  setup() {
    const chartCanvas = ref<HTMLCanvasElement | null>(null);

    onMounted(() => {
      if (chartCanvas.value) {
        new Chart(chartCanvas.value, {
          type: "pie",
          data: {
            labels: ["电脑", "手机", "家电", "家具", "其他"],
            datasets: [
              {
                label: "销售额",
                data: [1048, 735, 580, 484, 300],
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: "top",
              },
              tooltip: {
                enabled: true,
              },
            },
          },
        });
      }
    });

    return {
      chartCanvas,
    };
  },
});
</script>

<style scoped>
canvas {
  display: block;
  margin: auto;
  width: 600px;
  height: 400px;
}
</style>
