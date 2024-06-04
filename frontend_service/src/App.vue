<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div name="parent">
    <div name="header-grid">
      <header>
          <nav>
            <ul>
              <li><RouterLink to="/curator">Curator</RouterLink></li>
              <li><RouterLink to="/stats">Stats</RouterLink></li>
            </ul>
          </nav>
      </header>
    </div>
    <div name="content-grid" class="content-grid"><RouterView /></div>
  </div>
</template>


<style scoped>


.parent {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: repeat(5, 1fr);
  grid-column-gap: 8px;
  grid-row-gap: 8px;
  position: absolute;
}

nav {
  width:100%;
  text-align: center;
  border-radius: 6px;
}

.header-grid {
  grid-area: 1 / 1 / 2 / 2;
  position: top;
}

.content-grid {
  grid-area: 2 / 1 / 6 / 2;
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
