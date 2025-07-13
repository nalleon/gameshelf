package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Details;
/**
 * @author Nabil L. A. @nalleon
 */
public class PhotoReview extends Details {
    /**
     * Properties
     */
    private String type;

    /**
     * Full constructor of the class
     * @param id of the photo
     * @param name of the photo
     * @param additionalText of the photo
     * @param type of the photo
     */
    public PhotoReview(int id, String name, String additionalText, String type) {
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
