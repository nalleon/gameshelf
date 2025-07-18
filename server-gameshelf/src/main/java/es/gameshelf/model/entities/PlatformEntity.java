package es.gameshelf.model.entities;

import es.gameshelf.domain.abstracts.Classification;
/**
 * @author Nabil L. A. @nalleon
 */
public class PlatformEntity extends Classification {
    /**
     * Default constructor of the class
     */
    public PlatformEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the platform
     */
    public PlatformEntity(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the platform
     */
    public PlatformEntity(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the platform
     * @param name of the platform
     */
    public PlatformEntity(int id, String name) {
        super(id, name);
    }
}
