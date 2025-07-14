package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Classification;
/**
 * @author Nabil L. A. @nalleon
 */
public class Platform extends Classification {
    /**
     * Default constructor of the class
     */
    public Platform() {
    }

    /**
     * Constructor of the class
     * @param id of the platform
     */
    public Platform(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the platform
     */
    public Platform(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the platform
     * @param name of the platform
     */
    public Platform(int id, String name) {
        super(id, name);
    }
}
