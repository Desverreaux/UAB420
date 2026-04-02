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

    border-radius: 25px;

    width: 60%;
    height: 60%;
    background-color: #FFFFFF;

    display: flex;
    justify-content: center;
    align-items: center;

    z-index: 1000;

    animation: fadeIn 0.3s ease;
}

.modal {
    background-color: #FF0000;
    padding: 2rem;
    border-radius: 25px;
    max-height: 100%;
    max-width: 100%;
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