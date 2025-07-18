package es.gameshelf.model.entities;

import es.gameshelf.domain.abstracts.Details;
/**
 * @author Nabil L. A. @nalleon
 */
public class PhotoReviewEntity extends Details {
    /**
     * Properties
     */
    private String type;

    /**
     * Default constructor of the class
     */
    public PhotoReviewEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the photo
     */
    public PhotoReviewEntity(int id) {
        super(id);
    }


    /**
     * Constructor of the class
     * @param name of the photo
     * @param additionalText of the photo
     * @param type of the photo
     */
    public PhotoReviewEntity(String name, String additionalText, String type) {
        super(name, additionalText);
        this.type = type;
    }

    /**
     * Full constructor of the class
     * @param id of the photo
     * @param name of the photo
     * @param additionalText of the photo
     * @param type of the photo
     */
    public PhotoReviewEntity(int id, String name, String additionalText, String type) {
        super(id, name, additionalText);
        this.type = type;
    }

    /**
     * Getters and setters
     */
    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}
