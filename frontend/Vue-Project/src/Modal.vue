<template>
    <div v-if="show" class="overlay" @click.self="$emit('close')">
        <div class="modal">
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    props: ["show"],
    emits: ["close"]
}
</script>

<style scoped>
.overlay {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    width: 60%;
    height: 60%;

    border-radius: 24px;
    padding: 1.5rem;

    background-color: #d1603d;

    display: flex;
    /*justify-content: center;
    align-items: center;*/

    z-index: 1000;

    animation: fadeIn 0.3s ease;

    box-sizing: border-box;
}

.modal {
    position: relative;

    background-color: #a6b07e;

    padding: 2rem;
    border-radius: 16px;

    height: 100%;
    width: 100%;
    animation: fadeIn 0.3s ease;

}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.95);
    } to {
        opacity: 1;
    }
}
</style>