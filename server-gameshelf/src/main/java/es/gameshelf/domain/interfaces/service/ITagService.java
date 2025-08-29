package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Tag;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface ITagService {
    Tag add(String name);
    List<Tag> findAll();
    Tag findById(Integer id);
    Tag findByName(String name);
    boolean delete(Integer id);
    Tag update(Integer id, String name);
}
