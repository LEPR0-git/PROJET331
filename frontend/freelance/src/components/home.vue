<template>
  <section class="home">
    <!-- HERO -->
    <div class="hero">
      <div class="hero-content">
        <h1>
          🇨🇲 <span class="highlight">FreelanceCM</span> —  
          le Cameroun du travail libre 💪
        </h1>
        <p>
          Que tu sois coiffeuse à Douala, développeur à Yaoundé, maçon à Garoua ou couturière à Bafoussam,  
          ici, ton talent trouve des opportunités. FreelanceCM connecte <b>tous les travailleurs camerounais</b> à ceux qui ont besoin d’eux.
        </p>
        <div class="hero-buttons">
          <router-link to="/freelances" class="btn-primary">🔎 Trouver un prestataire</router-link>
          <router-link to="/inscription" class="btn-secondary">✨ Créer mon profil</router-link>
        </div>
      </div>
    </div>

    <!-- MÉTIERS -->
    <div class="categories">
      <h2>🧠 Les talents du pays sont ici !</h2>
      <p class="subtitle">De tous les coins du Cameroun, des femmes et des hommes qui bossent dur chaque jour.</p>
      <div class="cards">
        <div class="card" v-for="(job, i) in jobs" :key="i">
          <div class="emoji">{{ job.emoji }}</div>
          <h3>{{ job.title }}</h3>
          <p>{{ job.desc }}</p>
        </div>
      </div>
    </div>

    <!-- POURQUOI FREELANCECM -->
    <div class="why">
      <h2>💼 Pourquoi choisir FreelanceCM ?</h2>
      <div class="why-cards">
        <div class="why-card" v-for="(reason, i) in reasons" :key="i">
          <div class="icon">{{ reason.icon }}</div>
          <h3>{{ reason.title }}</h3>
          <p>{{ reason.desc }}</p>
        </div>
      </div>
    </div>

    <!-- COMMUNAUTÉ -->
    <div class="community">
      <h2>🇨🇲 Une communauté fière et solidaire</h2>
      <p>
        FreelanceCM, c’est plus qu’une plateforme : c’est une famille de travailleurs motivés,  
        qui se soutiennent, s’entraident et montrent au monde ce que le Cameroun sait faire !
      </p>
      <router-link to="/register" class="btn-primary">Rejoindre la communauté</router-link>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      jobs: [
        { emoji: '💻', title: 'Développeurs', desc: 'Des solutions numériques 100 % made in Cameroun.' },
        { emoji: '✂️', title: 'Coiffeurs & esthéticiens', desc: 'Le style et la beauté à la camerounaise.' },
        { emoji: '🧱', title: 'Maçons & plombiers', desc: 'Des bâtisseurs du pays, solides comme le béton !' },
        { emoji: '🎨', title: 'Graphistes & créatifs', desc: 'Des idées qui font vibrer les couleurs du pays.' },
        { emoji: '🍲', title: 'Cuisiniers & traiteurs', desc: 'Le bon goût du ndolé, du eru et de la passion !' },
        { emoji: '🚗', title: 'Mécaniciens & chauffeurs', desc: 'Toujours prêts à dépanner et avancer.' },
      ],
      reasons: [
        { icon: '🔥', title: 'Simple et rapide', desc: 'Crée ton profil, publie tes services et commence à travailler en quelques minutes.' },
        { icon: '🤝', title: 'Connexion locale', desc: 'Trouve facilement des clients près de toi, dans ta ville ou ta région.' },
        { icon: '💰', title: 'Gagne plus', desc: 'Valorise ton travail, fixe ton prix, sans intermédiaire.' },
        { icon: '📱', title: 'Accessible à tous', desc: 'Disponible sur téléphone, tablette et ordinateur.' }
      ]
    }
  }
}
</script>

<style scoped>
.home {
  color: white;
  background-color: #0f1f2d;
  font-family: "Poppins", sans-serif;
}

/* === HERO === */
.hero {
  background: linear-gradient(135deg, #007a5e, #1d2d3a);
  text-align: center;
  padding: 90px 20px;
  color: white;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 2.7rem;
  font-weight: 700;
  margin-bottom: 20px;
  line-height: 1.3;
}

.highlight {
  color: #ffe600;
}

.hero p {
  font-size: 1.15rem;
  line-height: 1.7;
  margin-bottom: 30px;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

/* Boutons */
.btn-primary,
.btn-secondary {
  padding: 13px 28px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: 0.3s ease;
}

.btn-primary {
  background-color: #ffe600;
  color: #1d2d3a;
}
.btn-primary:hover {
  background-color: #ffcc00;
}

.btn-secondary {
  border: 2px solid #ffe600;
  color: #ffe600;
}
.btn-secondary:hover {
  background-color: #ffe600;
  color: #1d2d3a;
}

/* === CATÉGORIES === */
.categories {
  background-color: #1d2d3a;
  text-align: center;
  padding: 70px 20px;
}

.categories h2 {
  font-size: 2.2rem;
  margin-bottom: 10px;
  color: #ffe600;
}

.subtitle {
  color: #c8c8c8;
  margin-bottom: 40px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 25px;
  max-width: 1000px;
  margin: 0 auto;
}

.card {
  background-color: #263845;
  padding: 25px;
  border-radius: 15px;
  transition: transform 0.2s ease, box-shadow 0.2s;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.emoji {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

/* === POURQUOI === */
.why {
  background-color: #0f1f2d;
  padding: 80px 20px;
  text-align: center;
}

.why h2 {
  color: #ffe600;
  font-size: 2rem;
  margin-bottom: 40px;
}

.why-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
  max-width: 1000px;
  margin: 0 auto;
}

.why-card {
  background-color: #1d2d3a;
  padding: 30px;
  border-radius: 12px;
  transition: transform 0.2s ease;
}
.why-card:hover {
  transform: translateY(-5px);
}
.icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

/* === COMMUNAUTÉ === */
.community {
  text-align: center;
  padding: 80px 20px;
  background: linear-gradient(135deg, #1d2d3a, #007a5e);
}

.community h2 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #ffe600;
}

.community p {
  max-width: 700px;
  margin: 0 auto 30px;
  line-height: 1.7;
  font-size: 1.1rem;
  color: #e8e8e8;
}

/* === Responsive === */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }
  .categories h2, .why h2, .community h2 {
    font-size: 1.6rem;
  }
}
</style>
