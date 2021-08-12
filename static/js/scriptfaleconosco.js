window.addEventListener("load", event => {

    var swiperWrapper = document.querySelector('.swiper-wrapper');

    /* The Team */
    var team = [{
            name: "Ana Trindade",
            role: "HTML/CSS e JS",
            desc: "Amo filmes, animes, sair com os amigos e tecnologia",
            photo: "../static/img/Ana.jpg",
            git: "https://github.com/anacgsantana",
            linkedin: "https://www.linkedin.com/in/ana-santanazt/",
        },
        {
            name: "Nikolas Furuta",
            role: "Back-End",
            desc:  "Gosto de filmes de terror e prefiro backend do que frontend",
            photo: "../static/img/img1.jpg",
            git: "mailto:rafaelavlucas@gmail.com",
            linkedin: "https://www.linkedin.com/in/nikolas-furuta/",
        },
        {
            name: "Marco Brito",
            role: "Banco de Dados",
            desc: "Não sabendo que era impossível foi lá e fez! backend.",
            photo: "../static/img/MarcoBrito.jpeg",
            git: "https://github.com/BritosMarcom",
            linkedin: "https://www.linkedin.com/in/marco-pereira-brito/",
        },
        {
            name: "Leo Acosta",
            role: "Banco de Dados",
            desc: "Uruguaio, apaixonado pelo futebol e a programação. Querendo se especializar em Back end!",
            photo: "../static/img/LeoAcosta.jpg",
            git: "https://github.com/LeoAcosta07",
            linkedin: "https://www.linkedin.com/in/leoacosta07/",
        },
        {
            name: "Antonio Carlos",
            role: "HTML/CSS e JS",
            desc: "Inimigo do batman.",
            photo: "../static/img/hqdefault.jpg",
            git: "https://github.com/daakotaz",
            linkedin: "https://www.linkedin.com/in/antonio-carlos-11950b177/",
        },
    ];

    /* Social Icons */
    var icons = [{
        iGit: "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg",
        iLinkedin: "https://rafaelalucas.com/dailyui/6/assets/linkedin.svg",
    }];

    var iGit = icons[0].iGit,
        iLinkedin = icons[0].iLinkedin;


    /* Function to populate the team members */
    function addTeam() {
        for (let i = 0; i < team.length; i++) {

            /* Variables for the team */
            var name = team[i].name,
                role = team[i].role,
                desc = team[i].desc,
                photo = team[i].photo,
                git = team[i].git,
                linkedin = team[i].linkedin;

            /* Template for the Team Cards */
            var template = `
                <div class="swiper-slide">
                <div class="card">
                    <span class="bg"></span>
                    <span class="more"></span>
                    <figure class="photo"><img src="${photo}"></figure>
                        <article class="text">
                            <p class="name">${name}</p>
                            <p class="role">${role}</p> 
                            <p class="desc">${desc}</p> 
                        </article>
                        
                        <div class="social">
                        <span class="pointer"></span>
                        <div class="icons">
                            
                            <a class="icon" href="${git}" target="_blank" data-index="1"><img src="${iGit}"></a>
                            <a class="icon" href="${linkedin}" target="_blank" data-index="2"><img src="${iLinkedin}"></a>                        
                            </div>
                            </div>
                    </div>
                </div>`;

            swiperWrapper.insertAdjacentHTML('beforeend', template);
        }
    };


    addTeam();



    /* Swiper Settings */

    var mySwiper = new Swiper(".swiper-container", {
        // Optional parameters
        direction: "horizontal",
        loop: true,
        centeredSlides: false,
        speed: 800,
        slidesPerView: 3,
        spaceBetween: 40,
        threshold: 5,


        // If we need pagination
        pagination: {
            el: ".swiper-pagination",
            clickable: true
        },

        // Navigation arrows
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev"
        },
        breakpoints: {
            1180: {
                slidesPerView: 2,
                spaceBetween: 40,
                centeredSlides: false,
            },
            799: {
                slidesPerView: 1,
                spaceBetween: 20,
                centeredSlides: true,
                loop: true,
            },
        }
    });

    /* Show More */

    var btnShow = document.querySelectorAll('.more');



    btnShow.forEach(function (el) {
        el.addEventListener('click', showMore);
    });

    function showMore(event) {
        var card = event.target.closest(".swiper-slide");

        if (card.classList.contains('show-more')) {
            card.classList.remove('show-more');
        } else {
            card.classList.add('show-more')
        }

    }


    /* Social Hover */
    var icon = document.querySelectorAll('.icon');

    icon.forEach(function (el) {
        el.addEventListener("mouseenter", followCursor);

    });


    function followCursor(event) {
        var pointer = event.currentTarget.closest(".swiper-slide").querySelector('.pointer'),
            index = event.currentTarget.dataset.index,
            sizeIcon = (60 * index) + 25;

        pointer.style.transform = `translateX(${sizeIcon}px)`;
    }


    /* end */
});