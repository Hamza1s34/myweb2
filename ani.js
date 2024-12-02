let scene, camera, renderer, robot, cube, sphere, torus;

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('scene-container').appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    const pointLight = new THREE.PointLight(0xffffff, 1);
    pointLight.position.set(25, 50, 25);
    scene.add(pointLight);

    // Robot
    const loader = new THREE.GLTFLoader();
    loader.load('https://threejs.org/examples/models/gltf/RobotExpressive/RobotExpressive.glb', (gltf) => {
        robot = gltf.scene;
        robot.scale.set(0.5, 0.5, 0.5);
        robot.position.set(0, -1, -5);
        scene.add(robot);

        // Add speech bubble
        const bubbleGeometry = new THREE.SphereGeometry(0.5, 32, 32);
        const bubbleMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
        const bubble = new THREE.Mesh(bubbleGeometry, bubbleMaterial);
        bubble.position.set(1, 1.5, 0);
        robot.add(bubble);

        const textGeometry = new THREE.TextGeometry('Welcome!', {
            font: new THREE.Font('helvetiker'),
            size: 0.1,
            height: 0.02,
        });
        const textMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
        const text = new THREE.Mesh(textGeometry, textMaterial);
        text.position.set(0.7, 1.4, 0.2);
        robot.add(text);
    });

    // Cube
    const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
    const cubeMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
    cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
    cube.position.set(-3, 0, -5);
    scene.add(cube);

    // Sphere
    const sphereGeometry = new THREE.SphereGeometry(0.5, 32, 32);
    const sphereMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
    sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    sphere.position.set(3, 0, -5);
    scene.add(sphere);

    // Torus
    const torusGeometry = new THREE.TorusGeometry(0.3, 0.1, 16, 100);
    const torusMaterial = new THREE.MeshPhongMaterial({ color: 0x0000ff });
    torus = new THREE.Mesh(torusGeometry, torusMaterial);
    torus.position.set(0, 2, -5);
    scene.add(torus);

    camera.position.z = 5;

    animate();
}

function animate() {
    requestAnimationFrame(animate);

    if (robot) {
        robot.rotation.y += 0.01;
    }

    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    sphere.rotation.y += 0.02;

    torus.rotation.x += 0.02;
    torus.rotation.y += 0.02;

    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener('resize', onWindowResize);

init();
