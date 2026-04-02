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
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #FFFFFF;

    display: flex;
    justify-content: center;
    align-items: center;

    z-index: 1000;
}

.modal {
    background-color: #FFFFFF;
    padding: 2rem;
    border-radius: 25px;
    min-width: 250px;
    max-width: 75%;
    animation: fadeIn 0.2s ease;
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