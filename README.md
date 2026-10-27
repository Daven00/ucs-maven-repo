# UCS Maven repository

Maven artifacts of the Usage Control framework (research code).
Provided for research purposes only, with no warranty and not intended
for production or security-critical use.

Each branch is published as a separate Maven repository:

- `rest` branch: `https://daven00.github.io/ucs-maven-repo/releases/rest/`
- `integration` branch: `https://daven00.github.io/ucs-maven-repo/releases/integration/`

Add the one you need to your `pom.xml`:

```
    <repositories>
      <repository>
        <id>ucs-public</id>
        <url>https://daven00.github.io/ucs-maven-repo/releases/rest/</url>
      </repository>
    </repositories>
```

The full list of versions is at https://daven00.github.io/ucs-maven-repo/