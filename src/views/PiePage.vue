<template>
  <div>
    <h2>{{ title }}</h2>
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
    <div class="chart-container">
      <canvas ref="barChartCanvas"></canvas>
    </div>
    <div class="chart-container">
      <canvas ref="lineChartCanvas"></canvas>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default defineComponent({
  name: 'PiePage',
  props: {
    title: {
      type: String,
      default: '饼状图',
    },
  },
  setup() {
    const chartCanvas = ref<HTMLCanvasElement | null>(null);
    const barChartCanvas = ref<HTMLCanvasElement | null>(null);
    const lineChartCanvas = ref<HTMLCanvasElement | null>(null);

    onMounted(() => {
      if (chartCanvas.value) {
        new Chart(chartCanvas.value, {
          type: 'pie',
          data: {
            labels: ['电脑', '手机', '家电', '家具', '其他'],
            datasets: [
              {
                label: '销售额',
                data: [1048, 735, 580, 484, 350],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              tooltip: {
                enabled: true,
              },
            },
          },
        });
      }

      if (barChartCanvas.value) {
        new Chart(barChartCanvas.value, {
          type: 'bar',
          data: {
            labels: ['一月', '二月', '三月', '四月', '五月', '六月'],
            datasets: [
              {
                label: '销售额',
                data: [500, 350, 450, 700, 600, 800],
                backgroundColor: '#36A2EB',
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              tooltip: {
                enabled: true,
              },
            },
          },
        });
      }

      if (lineChartCanvas.value) {
        new Chart(lineChartCanvas.value, {
          type: 'line',
          data: {
            labels: ['一月', '二月', '三月', '四月', '五月', '六月'],
            datasets: [
              {
                label: '销售额',
                data: [500, 350, 450, 700, 600, 800],
                borderColor: '#FF6384',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
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
      barChartCanvas,
      lineChartCanvas,
    };
  },
});
</script>

<style scoped>
.chart-container {
  position: relative;
  margin: auto;
  height: 50vh;
  width: 50vw;
}
</style>