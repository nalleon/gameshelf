package es.gameshelf.model.entities;

import es.gameshelf.domain.abstracts.Details;
/**
 * @author Nabil L. A. @nalleon
 */
public class RegionEntity extends Details {
    /**
     * Default constructor of the class
     */
    public RegionEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the region
     */
    public RegionEntity(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the region
     */
    public RegionEntity(String name) {
        super(name);
    }

    /**
     * Constructor of the class
     * @param name of the region
     * @param additionalText of the region
     */
    public RegionEntity(String name, String additionalText) {
        super(name, additionalText);
    }

    /**
     * Constructor of the class
     * @param id of the region
     * @param name of the region
     * @param additionalText of the region
     */
    public RegionEntity(int id, String name, String additionalText) {
        super(id, name, additionalText);
    }
}
